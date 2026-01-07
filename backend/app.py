from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///museum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 数据模型
class Artifact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    era = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    material = db.Column(db.String(50))
    description = db.Column(db.Text)
    discovered_date = db.Column(db.DateTime)
    exhibition_id = db.Column(db.Integer, db.ForeignKey('exhibition.id'))
    coordinates = db.Column(db.String(100))  # 经纬度坐标
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Exhibition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    exhibition_type = db.Column(db.String(50))  # long-term, temporary
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    visitor_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')
    artifacts = db.relationship('Artifact', backref='exhibition', lazy=True)


class HistoricalEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    year = db.Column(db.Integer)
    event_type = db.Column(db.String(50))  # political, cultural, economic
    location = db.Column(db.String(100))
    artifacts = db.relationship('ArtifactEvent', backref='historical_event', lazy=True)


class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    interaction_type = db.Column(db.String(50))  # view, repair, explore
    artifact_id = db.Column(db.Integer, db.ForeignKey('artifact.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # 秒


# 中间表：文物与历史事件关联
class ArtifactEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artifact_id = db.Column(db.Integer, db.ForeignKey('artifact.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('historical_event.id'))


# API路由
@app.route('/')
def index():
    return jsonify({
        'message': '时空博物馆 API',
        'version': '1.0.0',
        'endpoints': {
            '/api/artifacts': '获取文物列表',
            '/api/exhibitions': '获取展览列表',
            '/api/events': '获取历史事件',
            '/api/timeline': '获取时间轴数据',
            '/api/treasure': '获取镇馆之宝'
        }
    })


@app.route('/api/artifacts', methods=['GET'])
def get_artifacts():
    artifacts = Artifact.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'era': a.era,
        'location': a.location,
        'material': a.material,
        'description': a.description,
        'image_url': a.image_url,
        'coordinates': a.coordinates
    } for a in artifacts])


@app.route('/api/artifacts/<int:artifact_id>', methods=['GET'])
def get_artifact(artifact_id):
    artifact = Artifact.query.get_or_404(artifact_id)
    return jsonify({
        'id': artifact.id,
        'name': artifact.name,
        'era': artifact.era,
        'location': artifact.location,
        'material': artifact.material,
        'description': artifact.description,
        'image_url': artifact.image_url,
        'discovered_date': artifact.discovered_date.isoformat() if artifact.discovered_date else None,
        'exhibition': artifact.exhibition.title if artifact.exhibition else None
    })


@app.route('/api/exhibitions', methods=['GET'])
def get_exhibitions():
    exhibitions = Exhibition.query.filter_by(status='active').all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'type': e.exhibition_type,
        'visitor_count': e.visitor_count,
        'artifact_count': len(e.artifacts),
        'status': e.status
    } for e in exhibitions])


@app.route('/api/timeline', methods=['GET'])
def get_timeline():
    # 生成时间轴数据
    timeline_data = {
        'eras': [
            {'name': '新石器时代', 'start': -8000, 'end': -2000},
            {'name': '夏商周', 'start': -2070, 'end': -256},
            {'name': '秦汉', 'start': -221, 'end': 220},
            {'name': '魏晋南北朝', 'start': 220, 'end': 589},
            {'name': '隋唐', 'start': 581, 'end': 907},
            {'name': '宋元', 'start': 960, 'end': 1368},
            {'name': '明清', 'start': 1368, 'end': 1912},
            {'name': '近现代', 'start': 1912, 'end': 2024}
        ],
        'events': []
    }

    events = HistoricalEvent.query.all()
    for event in events:
        timeline_data['events'].append({
            'id': event.id,
            'title': event.title,
            'year': event.year,
            'type': event.event_type,
            'description': event.description[:100] + '...' if len(event.description) > 100 else event.description
        })

    return jsonify(timeline_data)


@app.route('/api/treasure', methods=['GET'])
def get_treasure():
    treasure = Artifact.query.filter_by(name='青铜鼎').first()
    if not treasure:
        treasure = Artifact.query.first()

    return jsonify({
        'name': treasure.name,
        'era': treasure.era,
        'location': treasure.location,
        'description': treasure.description,
        'material': treasure.material,
        'significance': '商代青铜礼器代表作，纹饰精美，工艺精湛，见证早期中华文明'
    })


@app.route('/api/map/markers', methods=['GET'])
def get_map_markers():
    artifacts = Artifact.query.filter(Artifact.coordinates.isnot(None)).all()
    markers = []

    for artifact in artifacts:
        if artifact.coordinates:
            lat, lng = map(float, artifact.coordinates.split(','))
            markers.append({
                'id': artifact.id,
                'name': artifact.name,
                'era': artifact.era,
                'coordinates': [lat, lng],
                'type': artifact.material
            })

    return jsonify(markers)


@app.route('/api/ai/explain', methods=['POST'])
def ai_explain():
    data = request.json
    question = data.get('question', '')
    artifact_id = data.get('artifact_id')

    # 简单的AI回应逻辑（实际项目中可集成真正的AI API）
    responses = {
        '历史背景': '这件文物出自商代晚期，是商王武丁时期的礼器，用于祭祀和宴会等重要场合。',
        '制作工艺': '采用范铸法工艺，先制作泥模，再制作外范和内芯，最后浇注青铜液。纹饰采用浮雕和阴刻相结合的手法。',
        '考古价值': '为研究商代礼制、铸造工艺和社会结构提供了重要实物资料。',
        '纹饰特点': '装饰有饕餮纹、云雷纹，是商代青铜器的典型风格。'
    }

    for key in responses:
        if key in question:
            return jsonify({
                'answer': responses[key],
                'sources': ['《中国青铜器研究》', '《商周考古》'],
                'confidence': 0.85
            })

    return jsonify({
        'answer': '根据我的知识库，这是一件重要的商代青铜器，具有很高的历史和文化价值。具体信息请参考相关考古文献。',
        'sources': [],
        'confidence': 0.65
    })


@app.route('/api/repair/puzzle', methods=['GET'])
def get_puzzle():
    return jsonify({
        'artifact_id': 1,
        'artifact_name': '青铜鼎',
        'pieces': [
            {'id': 1, 'type': 'corner', 'image': '/static/images/piece1.png'},
            {'id': 2, 'type': 'edge', 'image': '/static/images/piece2.png'},
            {'id': 3, 'type': 'edge', 'image': '/static/images/piece3.png'},
            {'id': 4, 'type': 'corner', 'image': '/static/images/piece4.png'},
        ],
        'complete_image': '/static/images/bronze_ding_complete.png',
        'difficulty': 'medium'
    })


@app.route('/api/repair/complete', methods=['POST'])
def complete_repair():
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    artifact_id = data.get('artifact_id')
    pieces_used = data.get('pieces_used', [])
    time_taken = data.get('time_taken', 0)

    # 记录修复完成
    interaction = UserInteraction(
        user_id=user_id,
        interaction_type='repair',
        artifact_id=artifact_id,
        duration=time_taken
    )
    db.session.add(interaction)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '修复完成！',
        'score': calculate_score(pieces_used, time_taken),
        'achievement': '青铜修复师'
    })


def calculate_score(pieces, time_taken):
    base_score = len(pieces) * 100
    time_bonus = max(0, 300 - time_taken) * 2  # 5分钟内完成有加分
    return base_score + time_bonus


# 初始化数据库
with app.app_context():
    db.create_all()

    # 添加示例数据
    if not Artifact.query.first():
        from datetime import datetime

        # 创建展览
        exhibition1 = Exhibition(
            title='商周青铜器',
            description='展示商周时期青铜器的精湛工艺与文化内涵',
            exhibition_type='long-term',
            visitor_count=23000
        )

        exhibition2 = Exhibition(
            title='唐宋瓷器',
            description='唐宋时期瓷器艺术的巅峰之作，展现东方美学',
            exhibition_type='temporary',
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 6, 30),
            visitor_count=18000
        )

        db.session.add_all([exhibition1, exhibition2])
        db.session.commit()

        # 创建文物
        artifacts = [
            Artifact(
                name='青铜鼎',
                era='商代',
                location='河南安阳',
                material='青铜',
                description='商代青铜礼器代表作，纹饰精美，工艺精湛',
                coordinates='36.099,114.392',
                exhibition_id=exhibition1.id,
                image_url='/static/images/bronze_ding.jpg'
            ),
            Artifact(
                name='青瓷莲花尊',
                era='唐代',
                location='陕西西安',
                material='陶瓷',
                description='唐代青瓷精品，莲花造型优雅',
                coordinates='34.341,108.939',
                exhibition_id=exhibition2.id,
                image_url='/static/images/celadon.jpg'
            )
        ]

        db.session.add_all(artifacts)

        # 历史事件
        events = [
            HistoricalEvent(
                title='商朝建立',
                description='商汤灭夏，建立商朝',
                year=-1600,
                event_type='political',
                location='河南商丘'
            ),
            HistoricalEvent(
                title='安阳殷墟发掘',
                description='大规模考古发掘，发现大量甲骨文和青铜器',
                year=1928,
                event_type='cultural',
                location='河南安阳'
            )
        ]

        db.session.add_all(events)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)