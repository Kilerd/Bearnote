from flask import *
from app.users.models import User
from app.note.models import Note

from app.users.decorators import require_login
from app.admin.decorators import require_admin

admin_module = Blueprint('admin_module', __name__)


@admin_module.route("/", methods=['GET'])
@require_login
@require_admin
def index_function():
    return '123'


@admin_module.route('/user', methods=['GET'])
@require_login
@require_admin
def user_function():
    all_user = User.objects()
    return render_template('admin/user.html', all_user=all_user)


@admin_module.route('/note', methods=['GET'])
@require_login
@require_admin
def note_function():
    all_note = Note.objects()
    return render_template('admin/note.html', all_note=all_note)
