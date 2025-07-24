from flask import Blueprint, request, jsonify
from flask_app import db
from flask_app.models.memory import Memory
from flask_app.utils.jwt_utils import token_required

memories_bp = Blueprint('memories', __name__, url_prefix='/memories')

@memories_bp.route('/', methods=['POST'])
@token_required
def create_memory(current_user):
    title = request.form.get('title')
    content = request.form.get('content')
    category = request.form.get('category')

    media = request.files.get('media')  
    voice = request.files.get('voice')

    if not title or not content:
        return jsonify({'error': 'Title and content are required.'}), 400

    media_url = None
    if media and media.filename != '' and allowed_file(media.filename):
        media_filename = secure_filename(media.filename)
        media_path = os.path.join(current_app.config['UPLOAD_FOLDER'], media_filename)
        media.save(media_path)
        media_url = f"/uploads/{media_filename}"

    voice_url = None
    if voice and voice.filename != '' and allowed_file(voice.filename):
        voice_filename = secure_filename(voice.filename)
        voice_path = os.path.join(current_app.config['UPLOAD_FOLDER'], voice_filename)
        voice.save(voice_path)
        voice_url = f"/uploads/{voice_filename}"

    new_memory = Memory(
        title=title,
        content=content,
        user_id=current_user.id,
        category=category,
        media_url=media_url,
        voice_url=voice_url
    )
    db.session.add(new_memory)
    db.session.commit()

    return jsonify({
        'message': f"{current_user.first_name}, your memory has been saved!",
        'memory': {
            'id': new_memory.id,
            'title': new_memory.title,
            'content': new_memory.content,
            'category': new_memory.category,
            'media_url': new_memory.media_url,
            'voice_url': new_memory.voice_url
        }
    }), 201

@memories_bp.route('/', methods=['GET'])
@token_required
def get_memories(current_user):
    category = request.args.get('category')

    query = Memory.query.filter_by(user_id=current_user.id)
    if category:
        query = query.filter_by(category=category)

    memories = query.all()

    base_url = request.host_url.rstrip('/')  # e.g., http://localhost:5000

    memory_list = [{
        'id': memory.id,
        'title': memory.title,
        'content': memory.content,
        'category': memory.category,
        'media_url': f"{base_url}/{memory.media_url.lstrip('/')}" if memory.media_url else None,
        'voice_url': f"{base_url}/{memory.voice_url.lstrip('/')}" if memory.voice_url else None,
        'created_at': memory.created_at,
        'updated_at': memory.updated_at
    } for memory in memories]

    return jsonify({
        'message': f"{current_user.first_name}, here are your memories.",
        'memories': memory_list
    })

@memories_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_memory(current_user, id):
    memory = Memory.query.filter_by(id=id, user_id=current_user.id).first()
    if not memory:
        return jsonify({'message': 'Memory not found'}), 404

    media_url = f"{request.host_url.rstrip('/')}{memory.media_url}" if memory.media_url else None
    voice_url = f"{request.host_url.rstrip('/')}{memory.voice_url}" if memory.voice_url else None

    return jsonify({
        'id': memory.id,
        'title': memory.title,
        'content': memory.content,
        'category': memory.category,
        'created_at': memory.created_at,
        'updated_at': memory.updated_at,
        'media_url': media_url,
        'voice_url': voice_url
    })

@memories_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_memory(current_user, id):
    memory = Memory.query.filter_by(id=id, user_id=current_user.id).first()
    if not memory:
        return jsonify({'message': 'Memory not found'}), 404

    if request.content_type.startswith('multipart/form-data'):
        title = request.form.get('title', memory.title)
        content = request.form.get('content', memory.content)
        category = request.form.get('category', memory.category)

        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            memory.media_url = f"/uploads/{filename}"
    else:
        data = request.json or {}
        title = data.get('title', memory.title)
        content = data.get('content', memory.content)
        category = data.get('category', memory.category)

    memory.title = title
    memory.content = content
    memory.category = category
    db.session.commit()

    return jsonify({
        'message': 'Memory updated successfully!',
        'memory': {
            'id': memory.id,
            'title': memory.title,
            'content': memory.content,
            'category': memory.category,
            'media_url': memory.media_url
        }
    }), 200

@memories_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_memory(current_user, id):
    memory = Memory.query.filter_by(id=id, user_id=current_user.id).first()
    if not memory:
        return jsonify({'message': 'Memory not found'}), 404

    db.session.delete(memory)
    db.session.commit()

    return jsonify({'message': 'Memory deleted successfully!'})


@memories_bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({'message': f"Access granted to user {request.user_id}"})

from werkzeug.utils import secure_filename
import os
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mp3', 'wav', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@memories_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    media = request.files.get('media')
    voice = request.files.get('voice')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        file_url = f"/uploads/{filename}"

        return jsonify({'message': 'File uploaded successfully', 'file_url': file_url}), 201

    return jsonify({'error': 'Invalid file type'}), 400
