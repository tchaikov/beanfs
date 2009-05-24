#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

import cgi

import logging
import datetime

import wsgiref.handlers

from google.appengine.ext import webapp

from view import base, group, image, item, main, order, user, vendor, purchase, event

webapp.template.register_template_library('filters')

application = webapp.WSGIApplication([
  (r'/', main.MainPage),
  (r'/u/(?P<username>.*)/profile', user.UserProfilePage),
  (r'/u/register', user.UserAddPage),        # TODO: need a complete impl of registration
  (r'/u/check-username', user.CheckAvailability),
  (r'/v/all', vendor.VendorListPage),          # will be replaced with the main page
  (r'/v/entry', vendor.VendorAddPage),
  (r'/v/(?P<vendor>.*)/item/list', item.ItemListPage),
  (r'/v/(?P<vendor>.*)/item/entry', item.ItemAddPage),
  (r'/o/(?P<txn>.*)/list', order.OrderListPage),
  (r'/o/(?P<txn>.*)/entry', order.OrderAddPage),
  (r'/o/(?P<txn>.*)/pay', order.OrderPayPage),
  (r'/g/(?P<group>.*)/profile', group.GroupProfilePage),
  (r'/g/add', group.GroupAddPage),
  (r'/g/list', group.GroupListPage),
  (r'/oops/(?P<error>.*)', base.ErrorPage),
  (r'/e/(?P<event>.*)/purchase', purchase.PurchasePage),
  (r'/e/(?P<event>.*)/entry', purchase.PurchasePage),
  (r'/e/(?P<event>.*)/list', purchase.EventList),
  (r'/e/(?P<event>.*)/close', purchase.EventClose),
  (r'/e/entry', event.AddPage),
  (r'/(image)/(\d+)', image.ImagePage),
  (r'/(thumb)/(\d+)', image.ImagePage),
  ], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
