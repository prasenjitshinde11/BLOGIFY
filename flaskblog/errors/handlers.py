from flask import Blueprint, render_template
import traceback

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    # Temporarily show full traceback for debugging on Render
    tb = traceback.format_exc()
    return f"<pre style='background:#111;color:#f88;padding:20px;font-size:13px;'><b>500 Error — Debug Info</b>\n\n{tb}</pre>", 500


