from random import uniform

import deliverysystem as d
import flask as f
import flask_googlemaps as fg
import os
import atexit


from apscheduler.schedulers.background import BackgroundScheduler


def orders():
    data = {}
    tnum = f.request.form["tnum"]
    result = d.ArticleData.query.get(tnum)
    result2 = d.DeliveryData.query.get(tnum)
    driver = None
    if result2 and result2.current_status == 'Shipping':
        driver = d.ECouriers.query.get(result2.driver_ID)
    if result:
        data['trackingNumber'] = result.trackingNumber
        data['Sender'] = result.sender
        data['Reciever'] = result.reciever
        if result.description:
            data['Description'] = result.description
        data['Weight'] = result.weight
        data["Priority"] = result2.priority
        data['Status'] = result2.current_status
        current_location = None
        if driver:
            if data["Status"] == 'Shipping':
                current_location = fg.Map(
                    identifier="View",
                    lat=driver.current_lat,
                    lng=driver.current_long,
                    markers=[(driver.current_lat, driver.current_long)]
                )
        try:
            if f.session['user']:
                order = []
                u = d.User.query.filter_by(username=f.session['user']).first()
                if u:
                    if u.packages:
                        for k in u.packages:
                            da = d.DeliveryData.query.get(k.trackingNumber)
                            dit = {"trackingNumber": k.trackingNumber, "Sender": k.sender, "Reciever": k.reciever,
                                   "Description": k.description, "Weight": k.weight, "Dangerous": k.dangerous_goods,
                                   "Priority": da.priority, "Status": da.current_status}
                            order.append(dit)
                        return f.render_template("pages/tracking.html", orders=order, data=data, map=current_location)
            return f.render_template("pages/tracking.html", data=data, map=current_location)
        except KeyError:
            return f.redirect(f.url_for('tracking'))
    return f.redirect(f.url_for('tracking'))


if not os.environ.get("WERKZEUG_RUN_MAIN") == "true":

    def lat_long_update():
        data = d.DeliveryData.query.all()
        if data:
            for order in data:
                driver = d.ECouriers.query.filter_by(driverid=order.driver_ID).first()
                data.current_lat = uniform(-180, 180)
                data.current_long = uniform(-90, 90)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lat_long_update, trigger="interval", minutes=5)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
