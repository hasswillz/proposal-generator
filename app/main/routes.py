# app/main/routes.py
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import os
from app.forms import ProposalForm # Assuming this is app/forms.py
from app.main import main_bp
from app.models import Proposal
from app import db
from app.ai_generator import generate_proposal # Assuming this module exists
from app.file_export import ProposalExporter # Assuming this module exists



@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ProposalForm()
    if form.validate_on_submit(): # Corrected to use form.validate_on_submit()
        try:
            # Convert form data to dict, excluding CSRF and submit
            proposal_data = {
                'project_name': form.project_name.data,
                'project_type': form.project_type.data,
                'description': form.description.data,
                'budget': float(form.budget.data),
                'duration_weeks': int(form.duration_weeks.data),
                'writing_style': form.writing_style.data,
                'complexity': form.complexity.data,
                'audience': form.audience.data,
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
            try:
                db.session.commit()
            except Exception as db_error:
                db.session.rollback()
                current_app.logger.error(f"Database commit failed: {str(db_error)}")
                if request.is_json:
                    return jsonify({
                        "status": "error",
                        "message": "Database save failed",
                        "debug": str(db_error)
                    }), 500
                flash('Database save failed. Please try again.', 'danger')
                return redirect(url_for('main.index'))


            if request.is_json:
                return jsonify({
                    'status': 'success',
                    'redirect': url_for('main.view_proposal', proposal_id=proposal.id)
                })
            flash('Proposal generated successfully!', 'success')
            return redirect(url_for('main.view_proposal', proposal_id=proposal.id))

        except ValueError as e:
            current_app.logger.error(f"Invalid data for proposal: {str(e)}")
            if request.is_json:
                return jsonify({
                    'status': 'error',
                    'message': f'Invalid data: {str(e)}'
                }), 400
            flash(f'Invalid data provided: {str(e)}', 'danger')

        except Exception as e:
            current_app.logger.error(f"Proposal generation error: {str(e)}")
            if request.is_json:
                return jsonify({
                    'status': 'error',
                    'message': 'Server error during proposal generation'
                }), 500
            flash('An unexpected error occurred during proposal generation.', 'danger')

    # If GET request or form validation failed for a POST request (and not JSON)
    if request.method == 'GET' or (request.method == 'POST' and not request.is_json):
        return render_template('main/index.html', form=form)
    elif request.method == 'POST' and request.is_json and not form.validate_on_submit():
        # Handle form validation errors for JSON requests
        return jsonify({
            'status': 'validation_error',
            'errors': form.errors
        }), 400


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
        os.makedirs(output_dir, exist_ok=True)

        filepath = export_methods[format](
            content=proposal.content,
            filename=filename, # Pass the full filename with extension
            output_dir=output_dir
        )

        return send_from_directory(
            directory=output_dir, # Use the actual directory where the file is saved
            path=os.path.basename(filepath), # Only the filename
            as_attachment=True
        )

    except Exception as e:
        current_app.logger.error(f"Export failed for proposal {proposal_id}, format {format}: {str(e)}")
        flash('Failed to generate download file. Please try again.', 'danger')
        return redirect(url_for('main.view_proposal', proposal_id=proposal_id))

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join('static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

