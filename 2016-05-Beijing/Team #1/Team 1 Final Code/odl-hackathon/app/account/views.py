from app import api
from flask import Flask, render_template, redirect, url_for, json, request
from . import account
from ..models import Account
from .. import db, ajax_dialog_view, ajax_refresh

VDC_DICT = {1: 'VDC1', 2: 'VDC2'}


@account.route('/')
def index():
    account_list = Account.query.all()
    return render_template('index.html', account_list=account_list, VDC_DICT=VDC_DICT)


@account.route('/create_acc', methods=['GET'])
def create_account():
    return ajax_dialog_view('create_acc.html', VDC_DICT=VDC_DICT)


@account.route('/create_acc', methods=['POST'])
def do_create_account():
    username = request.form['username']
    vdc = request.form['vdc']
    account = Account(username, vdc)
    db.session.add(account)
    db.session.commit()
    return redirect(url_for('account.index'))


@account.route('/checkin/<int:user_id>', methods=['GET'])
def checkin(user_id):
    return ajax_dialog_view('checkin_acc.html', user_id=user_id)


@account.route('/checkin', methods=['POST'])
def do_checkin():
    user_id = request.form['user_id']
    mac = request.form['mac']
    account = Account.query.filter_by(id=user_id).first()
    if account:
        api.simple_add_open_flow('openflow:3', 'in_' + account.user_name, int(mac[-1]) + 2, account.vdc_id)
        api.simple_add_open_flow('openflow:3', 'out_' + account.user_name, account.vdc_id, int(mac[-1]) + 2)

        # TODO
        api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp1', 1, [2, 3], add_ctrl=False)
        api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp2', 2, [1, 3], add_ctrl=False)
        api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp3', 3, [1, 2], add_ctrl=False)
        account.check_in_mac_addr = mac
        db.session.add(account)
        db.session.commit()

    return redirect(url_for('account.index'))


@account.route('/checkout/<int:user_id>')
def checkout(user_id):
    account = Account.query.filter_by(id=user_id).first()
    if account:
        api.del_open_flow('openflow:3', 'in_' + account.user_name)
        api.del_open_flow('openflow:3', 'out_' + account.user_name)

        # TODO
        #api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp1_' + account.user_name, 1, [2, 3], add_ctrl=False)
        #api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp2_' + account.user_name, 2, [1, 3], add_ctrl=False)
        #api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp3_' + account.user_name, 3, [1, 2], add_ctrl=False)
        account.check_in_mac_addr = None
        db.session.add(account)
        db.session.commit()

    return ajax_refresh()


@account.route('/delete/<int:user_id>')
def account_delete(user_id):
    account = Account.query.filter_by(id=user_id).first()
    if account:
        api.del_open_flow('openflow:3', 'in_' + account.user_name)
        api.del_open_flow('openflow:3', 'out_' + account.user_name)

        # TODO
        #api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp1_' + account.user_name, 1, [2, 3], add_ctrl=False)
        #api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp2_' + account.user_name, 2, [1, 3], add_ctrl=False)
        #api.simple_add_open_flow('openflow:%d' % account.vdc_id, 'tmp3_' + account.user_name, 3, [1, 2], add_ctrl=False)
        db.session.delete(account)
        db.session.commit()
    return ajax_refresh()
