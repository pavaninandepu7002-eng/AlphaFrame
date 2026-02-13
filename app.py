from flask import Flask, render_template, request, redirect, url_for, jsonify
from scriptoria.generator import generate
from scriptoria.storage import append_entry, read_history

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def do_generate():
    # Backwards-compatible form POST route (keeps original behavior)
    idea = request.form.get('idea', '').strip()
    mode = request.form.get('mode', 'screenplay')
    if not idea:
        return redirect(url_for('index'))
    output = generate(idea, mode)
    append_entry({'idea': idea, 'mode': mode, 'output': output})
    return render_template('result.html', idea=idea, mode=mode, output=output)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json() or {}
    idea = (data.get('idea') or '').strip()
    mode = data.get('mode', 'screenplay')
    temperature = data.get('temperature', 0.8)
    max_tokens = data.get('max_tokens', 800)
    project = data.get('project') or 'default'
    if not idea:
        return jsonify({'error': 'idea is required'}), 400
    output = generate(idea, mode, temperature=temperature, max_tokens=max_tokens)
    entry = {'project': project, 'idea': idea, 'mode': mode, 'output': output, 'temperature': temperature, 'max_tokens': max_tokens}
    append_entry(entry)
    return jsonify({'output': output, 'entry': entry})


@app.route('/api/history', methods=['GET'])
def api_history():
    project = request.args.get('project')
    history = read_history()
    if project:
        history = [h for h in history if (h.get('project') or 'default') == project]
    return jsonify(history)


@app.route('/api/history/clear', methods=['POST'])
def api_history_clear():
    from scriptoria.storage import clear_history
    clear_history()
    return jsonify({'ok': True})


@app.route('/api/history/<int:index>', methods=['DELETE'])
def api_history_delete(index):
    from scriptoria.storage import delete_entry
    delete_entry(index)
    return jsonify({'ok': True})


@app.route('/api/history/<int:index>/favorite', methods=['POST'])
def api_history_favorite(index):
    from scriptoria.storage import read_history, update_entry
    history = read_history()
    if not (0 <= index < len(history)):
        return jsonify({'error': 'not found'}), 404
    current = bool(history[index].get('favorite'))
    update_entry(index, {'favorite': not current})
    return jsonify({'ok': True, 'favorite': not current})


@app.route('/api/history/<int:index>/tags', methods=['POST'])
def api_history_tags(index):
    data = request.get_json() or {}
    tags = data.get('tags', [])
    if not isinstance(tags, list):
        return jsonify({'error': 'tags must be a list'}), 400
    from scriptoria.storage import read_history, update_entry
    history = read_history()
    if not (0 <= index < len(history)):
        return jsonify({'error': 'not found'}), 404
    update_entry(index, {'tags': tags})
    return jsonify({'ok': True, 'tags': tags})


@app.route('/api/stats', methods=['GET'])
def api_stats():
    from scriptoria.storage import stats
    return jsonify(stats())


if __name__ == '__main__':
    app.run(debug=True)
