
functionality
=============
* notify user to order meal at noon using IM or email
* add a 404 page
* allow user to submit multiple purchases in one batch
 - allow user edit his/her purchased items when submitting the purchase (e.g. comments, grouping), how about drag and drop?
* may need to separate models.Purchase into two models so that user can reuse his/her purchase
 - Purchase: item, fallbacks, notes
 - PurchaseEntry: customer, status, event, ReferenceProperty(Purchase)
* what is in an Order should not be purchases but confirmed items

UI
===
* use ajax to load items into the order page
* integrate with GoogleMap to find vendors around the user
* add a member in group page should reassemble igoogle's todo list, i.e. adding just in place.

restructure
===========
* use a customized jquery ui with minimum set of functionality (so far tab only)
* replace the User in group with google user, we will have User as the Account, and google user will be the connection key in these tables
* try to remove all trace of google db from view and control
* abstract the boilerplate stuff of RESTful into a class

Misc
====
* use ajax libraries hosted by ajax.googleapis.com, see http://code.google.com/apis/ajaxlibs/documentation/
