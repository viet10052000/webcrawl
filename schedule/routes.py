from flask import Flask, render_template, request, redirect, jsonify, flash
from app import app, login_required, roles_required, db
from schedule.models import Schedule
from datetime import datetime
@app.route('/schedule/list')
@login_required
@roles_required('admin','collector')
def schedule_list():
    lists = Schedule().index()
    for item in lists:
        item["tool"] = db.crawlproducts.find_one({"_id": item["crawlproduct_id"]})
        try:
            date_object = datetime.strptime(item["updated_at"]['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            item["updated_at"] = date_object.strftime('%Y-%m-%d %H:%M')
        except:
            item["updated_at"] = item["updated_at"].strftime('%Y-%m-%d %H:%M')
    return render_template('/adminv2/schedule/list.html',lists=lists)

@app.route('/schedule/create', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def schedule_create():
    if request.method == 'GET':
        categories = list(db.crawlproducts.find())
        return render_template('adminv2/schedule/create.html',categories=categories)
    elif request.method == 'POST':
        data = Schedule().create()
        if 'success' in data:
            flash('Thêm trình thu thập tự động thành công')
            return redirect('/schedule/list')
        flash(data)
        return redirect('/schedule/create')

@app.route('/schedule/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def schedule_edit(id):
    if request.method == 'GET':
        category = db.schedules.find_one({ '_id' : id })
        categories = list(db.crawlproducts.find())
        return render_template('adminv2/schedule/edit.html', category=category, categories=categories)
    elif request.method == 'POST':
        data = {
            "_id" : id,
            "crawlproduct_id": request.values.get('crawlproduct_id'),
            "time_repeat": request.values.get('time_repeat'),
            "updated_at": datetime.now()
        }
        schedule = Schedule().update(id,data)
        if schedule == 'success':
            flash('Sửa trình thu thập tự động thành công')
            return redirect('/schedule/list')
        flash(schedule)
        return redirect('/schedule/edit/' + id)
    
@app.route('/schedule/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def schedule_delete(id):
    lists = Schedule().delete(id)
    flash('Xóa trình thu thập tự động thành công')
    return redirect('/schedule/list')