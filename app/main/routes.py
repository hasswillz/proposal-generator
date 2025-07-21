# app/main/routes.py
from flask import (render_template, redirect, url_for, flash, request, current_app,
                   send_from_directory, jsonify, session)
from flask_login import login_required, current_user
from datetime import datetime
from os import abort, path, makedirs
from app.forms import ProposalForm # Assuming this is app/forms.py
from app.main import main_bp
from app.models import Proposal
from app import db
from werkzeug.utils import redirect
from urllib.parse import urlparse
from app.ai_generator import generate_proposal # Assuming this module exists
from app.file_export import ProposalExporter # Assuming this module exists


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ProposalForm()
    if form.validate_on_submit():
        try:
            proposal_data = {
                'project_name': form.project_name.data,
                'project_type': form.project_type.data,
                'description': form.description.data,
                'budget': float(form.budget.data),
                'duration_weeks': int(form.duration_weeks.data),
                'writing_style': form.writing_style.data,
                'complexity': form.complexity.data,
                'audience': form.audience.data,
                'mobile_number': form.mobile_number.data,
                'contact_email': form.contact_email.data
            }

            proposal_content = generate_proposal(proposal_data)

            proposal = Proposal(
                title=proposal_data['project_name'],
                content=proposal_content,
                author=current_user,
                generated_at=datetime.utcnow(),
                # Assuming these fields exist in Proposal model for dashboard display
                project_type=proposal_data['project_type']
            )

            db.session.add(proposal)
            db.session.commit()

            if request.is_json:  # AJAX request
                return jsonify({
                    'status': 'success',
                    'redirect': url_for('main.dashboard', _external=True)
                }), 200
            else:  # Regular form submission
                return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500
            flash(f'Error: {str(e)}', 'danger')

    return render_template('main/index.html', form=form)


@main_bp.route('/about') # Removed POST method if it's just an informational page
def about():
    return render_template('main/about.html') # Removed form=ProposalForm() if not needed on about page


@main_bp.route('/dashboard')
@login_required
def dashboard():
    proposals = db.session.query(Proposal)\
                  .filter_by(user_id=current_user.id)\
                  .order_by(Proposal.generated_at.desc())\
                  .all()
    return render_template('main/dashboard.html', proposals=proposals)


@main_bp.route('/proposal/<int:proposal_id>')
@login_required
def view_proposal(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    # Ensure only the owner can view their proposals, or admin roles if applicable
    if proposal.user_id != current_user.id:
        flash('You are not authorized to view this proposal.', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('main/proposal.html', proposal=proposal, datetime=datetime)


@main_bp.route('/download/<int:proposal_id>/<format>')
@login_required
def download_proposal(proposal_id, format):
    proposal = Proposal.query.get_or_404(proposal_id)
    # Ensure only the owner can download their proposals
    if proposal.user_id != current_user.id:
        flash('You are not authorized to download this proposal.', 'danger')
        return redirect(url_for('main.dashboard'))

    filename = f"proposal_{proposal_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{format}" # Added timestamp for unique filenames
    valid_formats = ['pdf', 'docx', 'md']

    if format not in valid_formats:
        flash(f'Invalid format requested: {format}', 'danger') # Show invalid format
        return redirect(url_for('main.view_proposal', proposal_id=proposal_id))

    try:
        export_methods = {
            'pdf': ProposalExporter.export_pdf,
            'docx': ProposalExporter.export_docx,
            'md': ProposalExporter.export_markdown
        }

        # Ensure the output directory exists
        output_dir = current_app.config.get('UPLOAD_FOLDER', 'temp_downloads')
        makedirs(output_dir, exist_ok=True)

        filepath = export_methods[format](
            content=proposal.content,
            filename=filename, # Pass the full filename with extension
            output_dir=output_dir
        )

        return send_from_directory(
            directory=output_dir, # Use the actual directory where the file is saved
            path=path.basename(filepath), # Only the filename
            as_attachment=True
        )

    except Exception as e:
        current_app.logger.error(f"Export failed for proposal {proposal_id}, format {format}: {str(e)}")
        flash('Failed to generate download file. Please try again.', 'danger')
        return redirect(url_for('main.view_proposal', proposal_id=proposal_id))

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        path.join('static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@main_bp.route('/set_language/<language>')
def set_language(language):
    if language not in current_app.config['LANGUAGES']:
        abort(400, "Invalid language")

    session['language'] = language
    flash(f"Language set to {current_app.config['LANGUAGES'][language]}", 'success')

    # Secure redirect back
    next_page = request.referrer or url_for('main.index')
    return redirect(next_page)