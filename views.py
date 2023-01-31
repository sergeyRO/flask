from flask.views import MethodView
from flask import jsonify, request
from database import Session, Ads
from errors import ApiException


class AdsView(MethodView):
    def get(self, id: int):
        with Session() as session:
            ads = session.query(Ads).get(id)
            if ads is None:
                raise ApiException(404, 'Not Found ads!')
        return jsonify({
            'id': ads.id,
            'title': ads.title,
            'desc': ads.desc,
            'created_at': ads.created_at,
            'id_user': ads.id_user
        })

    def post(self):
        data_ads = request.json
        with Session() as session:
            new_ads = Ads(**data_ads)
            session.add(new_ads)
            session.commit()
            return jsonify({'id_ads': new_ads.id, 'title': new_ads.title, 'created_at': new_ads.created_at})

    def patch(self, id: int):
        data_ads = request.json
        with Session() as session:
            ads = session.query(Ads).get(id)
            for field, value in data_ads.items():
                setattr(ads, field, value)
            session.add(ads)
            session.commit()
            return jsonify({'id': ads.id, 'title': ads.title, 'desc': ads.desc})

    def delete(self, id: int):
        with Session() as session:
            ads = session.query(Ads).get(id)
            session.delete(ads)
            session.commit()
            return jsonify({'status': 'deleted'})
