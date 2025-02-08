"""SpareHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from django.urls import re_path as url
from Admin import views as admin_view
from User import views as user_view
from Spare_Parts_Shop import views as Sshop_view
from Workshop import views as Wshop_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',admin_view.index,name='index'),
    url(r'^login/',admin_view.login,name='login'),
    url(r'^loginAction/',admin_view.loginAction,name='loginAction'),
    url(r'^addBrand/',admin_view.addBrand,name='addBrand'),
    url(r'^addBrandAction/',admin_view.addBrandAction,name='addBrandAction'),
    url(r'^addModel/',admin_view.addModel,name='addModel'),
    url(r'^getBrand/',admin_view.getBrand,name='getBrand'),
    url(r'^addModelAction/',admin_view.addModelAction,name='addModelAction'),
    url(r'^shopSignup/',Sshop_view.shopSignup,name='shopSignup'),
    url(r'^shopSignupAction/',Sshop_view.shopSignupAction,name='shopSignupAction'),
    url(r'^viewSpareShop/',admin_view.viewSpareShop,name='viewSpareShop'),
    url(r'^approveSpareShop/(?P<sid>\d+)/$',admin_view.approveSpareShop,name='approveSpareShop'),
    url(r'^rejectSpareShop/(?P<sid>\d+)/$',admin_view.rejectSpareShop,name='rejectSpareShop'),
    url(r'^addSpareParts/',Sshop_view.addSpareParts,name='addSpareParts'),
    url(r'^getModel/',Sshop_view.getModel,name='getModel'),
    url(r'^addSparePartsAction/',Sshop_view.addSparePartsAction,name='addSparePartsAction'),
    url(r'^removeSpareShop/(?P<sid>\d+)/$',admin_view.removeSpareShop,name='removeSpareShop'),
    url(r'^viewSpareParts/',Sshop_view.viewSpareParts,name='viewSpareParts'),
    url(r'^updateSparePart/(?P<pid>\d+)/$',Sshop_view.updateSparePart,name='updateSparePart'),
    url(r'^updateSparePartAction/',Sshop_view.updateSparePartAction,name='updateSparePartAction'),
    url(r'^deleteSparePart/(?P<pid>\d+)/$',Sshop_view.deleteSparePart,name='deleteSparePart'),
    url(r'^userSignup/',user_view.userSignup,name='userSignup'),
    url(r'^userSignupAction/',user_view.userSignupAction,name='userSignupAction'),
    url(r'^viewSparePartsUser/',user_view.viewSparePartsUser,name='viewSparePartsUser'),
    url(r'^addToCart/(?P<pid>\d+)/$',user_view.addToCart,name='addToCart'),
    url(r'^addToCartAction/',user_view.addToCartAction,name='addToCartAction'),
    url(r'^viewCart/',user_view.viewCart,name='viewCart'),
    url(r'^selectOrder/(?P<cid>\d+)/$',user_view.selectOrder,name='selectOrder'),
    url(r'^addOrder/',user_view.addOrder,name='addOrder'),
    url(r'^viewOrders/',Sshop_view.viewOrders,name='viewOrders'),
    url(r'^orderDetails/(?P<oid>\d+)/$',Sshop_view.orderDetails,name='orderDetails'),
    url(r'^approveOrder/(?P<oid>\d+)/$',Sshop_view.approveOrder,name='approveOrder'),
    url(r'^rejectOrder/(?P<oid>\d+)/$',Sshop_view.rejectOrder,name='rejectOrder'),
    url(r'^orderStatus/$',user_view.orderStatus,name='orderStatus'),
    url(r'^payForOrder/(?P<oid>\d+)/(?P<page>\d+)/$',user_view.payForOrder,name='payForOrder'),
    url(r'^payForOrderAction/',user_view.payForOrderAction,name='payForOrderAction'),
    url(r'^paymentDetails/(?P<oid>\d+)/$',Sshop_view.paymentDetails,name='paymentDetails'),
    url(r'^salesReport/',admin_view.salesReport,name='salesReport'),
    url(r'^getTransactions/',admin_view.getTransactions,name='getTransactions'),
    url(r'^addTrackingDetails/(?P<oid>\d+)/(?P<page>\d+)/$',Sshop_view.addTrackingDetails,name='addTrackingDetails'),
    url(r'^addTrackingDetailsAction/',Sshop_view.addTrackingDetailsAction,name='addTrackingDetailsAction'),
    url(r'^viewTrackingDetails/(?P<oid>\d+)/$',user_view.viewTrackingDetails,name='viewTrackingDetails'),
    url(r'^cancelOrder/(?P<oid>\d+)/(?P<page>\d+)/$',user_view.cancelOrder,name='cancelOrder'),
    url(r'^verifyCancelling/(?P<oid>\d+)/(?P<page>\d+)/$',Sshop_view.verifyCancelling,name='verifyCancelling'),
    url(r'^getSpareParts/',user_view.getSpareParts,name='getSpareParts'),
    url(r'^searchSparePart/',user_view.searchSparePart,name='searchSparePart'),
    #url(r'^giveRatingAndReview/',user_view.giveRatingAndReview,name='giveRatingAndReview'),
    url(r'^rateAndReview/(?P<oid>\d+)/$',user_view.rateAndReview,name='rateAndReview'),
    url(r'^rateAndReviewAction/',user_view.rateAndReviewAction,name='rateAndReviewAction'),
    url(r'^viewReview/(?P<pid>\d+)/$',user_view.viewReview,name="viewReview"),
    url(r'^viewPaymentDetails/(?P<oid>\d+)/$',user_view.viewPaymentDetails,name='viewPaymentDetails'),
    url(r'^writeComplaint/',user_view.writeComplaint,name='writeComplaint'),
    url(r'^writeComplaintAction/',user_view.writeComplaintAction,name='writeComplaintAction'),
    url(r'^deleteFromCart/(?P<cid>\d+)/$',user_view.deleteFromCart,name='deleteFromCart'),
    url(r'^viewComplaints/',admin_view.viewComplaints,name='viewComplaints'),
    url(r'^complaintDetails/(?P<cid>\d+)/$',admin_view.complaintDetails,name='complaintDetails'),
    url(r'^deleteComplaint/(?P<cid>\d+)/$',admin_view.deleteComplaint,name='deleteComplaint'),
    url(r'^updateProfile/',user_view.updateProfile,name='updateProfile'),
    url(r'^updateProfileAction/',user_view.updateProfileAction,name='updateProfileAction'),
    url(r'^updateProfileShop/',Sshop_view.updateProfileShop,name='updateProfileShop'),
    url(r'^updateProfileShopAction/',Sshop_view.updateProfileShopAction,name='updateProfileShopAction'),
    url(r'^notification/',user_view.notification,name='notification'),
    url(r'^readNotification/(?P<nid>\d+)/$',user_view.readNotification,name='readNotification'),
    url(r'^workshopSignup/',Wshop_view.workshopSignup,name='workshopSignup'),
    url(r'^workshopSignupAction/',Wshop_view.workshopSignupAction,name='workshopSignupAction'),
    url(r'^viewWorkshop/',admin_view.viewWorkshop,name='viewWorkshop'),
    url(r'^approveWorkshop/(?P<wid>\d+)/$',admin_view.approveWorkshop,name='approveWorkshop'),
    url(r'^rejectWorkshop/(?P<wid>\d+)/$',admin_view.rejectWorkshop,name='rejectWorkshop'),
    url(r'^removeWorkshop/(?P<wid>\d+)/$',admin_view.removeWorkshop,name='removeWorkshop'),
    url(r'^updateProfileWorkshop/',Wshop_view.updateProfileWorkshop,name='updateProfileWorkshop'),
    url(r'^updateProfileWorkshopAction/',Wshop_view.updateProfileWorkshopAction,name='updateProfileWorkshopAction'),
    url(r'^addService/',Wshop_view.addService,name='addService'),
    url(r'^addServiceAction/',Wshop_view.addServiceAction,name='addServiceAction'),
    url(r'^viewServicesByWorkshop/',Wshop_view.viewServicesByWorkshop,name='viewServicesByWorkshop'),
    url(r'^updateService/(?P<sid>\d+)/$',Wshop_view.updateService,name='updateService'),
    url(r'^deleteService/(?P<sid>\d+)/(?P<page>\d+)/$',Wshop_view.deleteService,name='deleteService'),
    url(r'^updateServiceAction/',Wshop_view.updateServiceAction,name='updateServiceAction'),
    url(r'^nearbyWorkshop/',user_view.nearbyWorkshop,name='nearbyWorkshop'),
    url(r'^viewServices/(?P<wid>\d+)/$',user_view.viewServices,name='viewServices'),
    url(r'^viewWorkShopReviews/(?P<wid>\d+)/$',user_view.viewWorkshopReviews,name='viewWorkshopReviews'),
    url(r'^addReviewForWorkshop/',user_view.addReviewForWorkshop,name='addReviewForWorkshop'),
    #url(r'^loadReviews/',user_view.loadReviews,name='loadReviews'),
    url(r'^viewReviewsByWorkshop/',Wshop_view.viewReviewsByWorkshop,name='viewReviewsByWorkshop'),
    url(r'^viewSparePartReview/(?P<pid>\d+)/$',Sshop_view.viewSparePartReview,name='viewSparePartReview'),
    url(r'^forgotPassword/',admin_view.forgotPassword,name='forgotPassword'),
    url(r'^getNext/',admin_view.getNext,name='getNext'),
    url(r'^changePasswordAction/',admin_view.changePasswordAction,name='changePasswordAction'),
    url(r'^validateShopData/',admin_view.validateShopData,name='validateShopData'),
    url(r'^validateUserData/',admin_view.validateUserData,name='validateUserData'),
    url(r'^getState/',Sshop_view.getState,name='getState'),
    url(r'^getDistrict/',Sshop_view.getDistrict,name='getDistrict'),
    url(r'^shopDetails/(?P<sid>\d+)/$',admin_view.shopDetails,name='shopDetails'),
    url(r'^workshopDetails/(?P<sid>\d+)/$',admin_view.workshopDetails,name='workshopDetails'),
    url(r'^getNearbyWorkshop/',user_view.getNearbyWorkshop,name='getNearbyWorkshop'),
    url(r'^addCategory/',admin_view.addCategory,name='addCategory'),
    url(r'^addCategoryAction/',admin_view.addCategoryAction,name='addCategoryAction'),
    url(r'^getCategory/',Sshop_view.getCategory,name='getCategory'),
    url(r'^partDetails/(?P<pid>\d+)/$',user_view.partDetails,name='partDetails'),
    url(r'^prebook/(?P<pid>\d+)/$',user_view.prebook,name='prebook'),
    url(r'^prebookAction/',user_view.prebookAction,name='prebookAction'),
    url(r'^viewPrebookings/',Sshop_view.viewPrebookings,name='viewPrebookings'),
    url(r'^approvePrebook/(?P<pid>\d+)/(?P<page>\d+)/$',Sshop_view.approvePrebook,name='approvePrebook'),
    url(r'^rejectPrebook/(?P<pid>\d+)/(?P<page>\d+)/$',Sshop_view.rejectPrebook,name='rejectPrebook'),
    url(r'^prebookingStatus/',user_view.prebookingStatus,name='prebookingStatus'),
    url(r'^orderPrebook/(?P<pid>\d+)/$',user_view.orderPrebook,name='orderPrebook'),
    url(r'^cancelPrebook/(?P<pid>\d+)/$',user_view.cancelPrebook,name='cancelPrebook'),
    url(r'^confirmOrderAction/',user_view.confirmOrderAction,name='confirmOrderAction'),
    url(r'^sparePartFromCategory/(?P<cid>\d+)/$',user_view.sparePartFromCategory,name='sparePartFromCategory'),
    url(r'^cancelConfirm/',user_view.cancelConfirm,name='cancelConfirm'),
    url(r'^searchSparePartByShop/',Sshop_view.searchSparePartByShop,name='searchSparePartByShop'),
    url(r'^updateStatus/(?P<pid>\d+)/$',admin_view.updateStatus,name='updateStatus'),
    url(r'^compareProduct/',user_view.compareProduct,name='compareProduct'),
    url(r'^replyAction/',admin_view.replyAction,name='replyAction'),
    url(r'^readReply/(?P<rid>\d+)/$',user_view.readReply,name='readReply'),
    url(r'^viewCategory/',admin_view.viewCategory,name='viewCategory'),
    url(r'^updateCategory/(?P<cid>\d+)/$',admin_view.updateCategory,name='updateCategory'),
    url(r'^editCategoryAction/',admin_view.editCategoryAction,name='editCategoryAction'),
    url(r'^viewBrand/',admin_view.viewBrand,name='viewBrand'),
    url(r'^updateBrand/(?P<bid>\d+)/$',admin_view.updateBrand,name='updateBrand'),
    url(r'^editBrandAction/',admin_view.editBrandAction,name='editBrandAction'),
    url(r'^deleteBrand/(?P<bid>\d+)/$',admin_view.deleteBrand,name='deleteBrand'),
    url(r'^viewModel/',admin_view.viewModel,name='viewModel'),
    url(r'^updateModel/(?P<mid>\d+)/$',admin_view.updateModel,name='updateModel'),
    url(r'^editModelAction/',admin_view.editModelAction,name='editModelAction'),
    url(r'^deleteModel/(?P<mid>\d+)/$',admin_view.deleteModel,name='deleteModel'),
    url(r'^getPartNames/',user_view.getPartNames,name='getPartNames'),
    url(r'^getPlace/',user_view.getPlace,name='getPlace'),
    url(r'^checkUsername/',admin_view.checkUsername,name='checkUsername'),
    url(r'^checkUsernameUpdate/',admin_view.checkUsernameUpdate,name='checkUsernameUpdate'),
    url(r'^getModelDrop/',admin_view.getModelDrop,name='getModelDrop'),
    url(r'^logout/',admin_view.logout,name='logout'),
    
    
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
