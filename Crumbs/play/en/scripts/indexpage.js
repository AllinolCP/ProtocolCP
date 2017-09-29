//To allow cross sub domain scripting
document.domain = 'clubpenguin.com';
var Disney = Disney || {};

/**
 ** Functions called from Club Penguin client via ExternalInterface
 **/
// Name Resubmission
function nameResubmission(player_id, token, data) {
  newHostname = location.hostname.replace("play","secured");
  newProtocol = ((newHostname.indexOf("sandbox") >= 0) ? "http" : "https");
  var href = newProtocol + "://" + newHostname + "/" + Disney.Play.langPath + "penguin/update-username/" + player_id + "/" + token + "/" + data;
  Disney.Play.showModal(href);
}

// Resend Activation Email (update parent email address if address provided different from one on file
function sendActivationEmailTo(parentEmailAddress, token, data) {
  newHostname = location.hostname.replace("play","secured");
  newProtocol = ((newHostname.indexOf("sandbox") >= 0) ? "http" : "https");
  var request = jQuery.ajax({
                    type: "POST",
                    url: newProtocol + "://" + newHostname + "/penguin/resend-activation-email",
                    data: {"parentEmailAddress": parentEmailAddress, "token": token, "data": data},
                    async: false,
                    dataType: 'text',
                    crossDomain: true,
                    success: function(result) {
                      $("#club_penguin")[0].handleSendActivationEmailTo(result);
                    }
                 });
}

// Membership Trial Banner
function showTrialBanner(daysRemaining) {		
  Disney.Play.daysLeft = daysRemaining;
  $('#BannerContainer').load("http://play.clubpenguin.com/"+Disney.Play.langPath+'trialbanner.htm',"",Disney.Play.setTrialBanner);
}

// Pre Activated Play Banner
function showActivationBanner(hoursRemaining) {		
  Disney.Play.daysLeft = Math.ceil(hoursRemaining / 24);
  Disney.Play.hoursLeft = Math.ceil(hoursRemaining);
  $('#BannerContainer').addClass("pre-activated");
  $('#BannerContainer').load("http://play.clubpenguin.com/"+Disney.Play.langPath+'preactivated-banner.htm',"",Disney.Play.setActivateBanner);
}

// Membership Expire Banner
function showMembershipBanner(swid) {
  newHostname = location.hostname.replace("play","secured");
  newProtocol = ((newHostname.indexOf("sandbox") >= 0) ? "http" : "https");
  var request = jQuery.ajax({
                    url: "http://" + location.hostname + "/web_service/membership.php?action=check",
                    data: '{"swid": "'+swid+'"}',
                    type: "post",
                    dataType: "json",
                    processData: false,
                    success: function(result) {
                      result = JSON.parse(result)
                      if (result.membershipExpiring) {
                        if (result.membership_banner.content.show) {
                          Disney.Play.daysLeft = result.daysRemaining;
                          $('#BannerContainer').load("http://play.clubpenguin.com/"+Disney.Play.langPath+'membershipbanner.htm',"",Disney.Play.setMembershipBanner);
                        }
                        //only slotted into test if membership is expiring.
                        window.metrics.setSWID(swid);
                        window.metrics.testImpression("MembershipBanner", result.membership_banner.isControl, result.membership_banner.variantIndex);
                      }
                    }
                 });  
}


function TrialBannerLink() {
  window.metrics.log('game_action', {'context':'membership_trial', 'action':'about_banner'});
}

// Successful creation of a Penguin
function penguinCreateSuccessCallback(swid) {
  try {
    // MediaMind tracking for UK Campaign
    // Only do this if cpMM cookie is set
    var cpMMcookie = getCookie('cpMM');
    if (cpMMcookie == 'true') {
      var transActivityId = '158295';
      var transRevenue = '';
      var transProductId = window.metrics.options.TRANSID;
      var transProductInfo = '';
      Disney.Play.addTracking(transActivityId, transRevenue, swid, transProductId, transProductInfo);
    }
  } catch (e) {}
}

jQuery(document).ready(function() {
  Disney.Play = Disney.Play || {};
  Disney.Membership = Disney.Play; //Alias used by lightbox close
  
	Disney.Play.setBigScreen = function() {
		$("#bigscreen").hide();
		$("#smallscreen").show();
		$("#D_F_GameSection").css("height", "95%");	
		
		// If D_F_HudNotification dom element has been created fix it's position
		if ($("#D_F_HudNotification").size() > 0) {
			Disney.Friends.UI.HudNotification.reposition();
		}
		
		try {
			window.metrics.log("game_action", {"action":"screen_resize", "context":"small_to_large"});
		} catch (e) {
		}
	}

	Disney.Play.setSmallScreen = function() {
		$("#smallscreen").hide();
		$("#bigscreen").show();
		$("#D_F_GameSection").css("height", "550px");		

		// If D_F_HudNotification dom element has been created fix it's position
		if ($("#D_F_HudNotification").size() > 0) {
			Disney.Friends.UI.HudNotification.reposition();
		}
		
		try {
			window.metrics.log("game_action", {"action":"screen_resize", "context":"large_to_small"});
		} catch (e) {
		}
	}

  Disney.Play.centerError = function(errorID) {
    var top = $(window).height() / 2 - 110;
    if (top < 0) {
      top = 0;
    }
    var left = $(window).width() / 2 - 177;
    if (left < 0) {
      left = 0;
    }
    $(errorID).css("top", top.toString() + "px").css("left", left.toString() + "px");
  }
  Disney.Play.stopEvent = function(event) {
    if (event.cancelable) {
      event.preventDefault();
    }
    event.cancelBubble = true;
    if (event.stopPropagation) {
      event.stopPropagation();
    }
  }

  Disney.Play.initModal = function() {
    Disney.Play.modal = new CP.utils.Modal({
      showClose: false,
      overlayClickClose: false, //too easy to accidentally close the lightbox with no way to reopen.
      contentCloseDelegate: '.modal-close',
      onOpenComplete: function() {},
      onCloseComplete: function() {},
      onCloseStart: function() {},
      onOpenStart: function() {}
    });
  };

  Disney.Play.showModal = function(url) {
    var rdm = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) { var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8); return v.toString(16); });
    html = '<iframe id="modal-iframe" src="'+url+'?'+rdm+'" height="500" width="500" allowtransparency="true" marginheight="0" marginwidth="0" frameborder="0" style="overflow:hidden;" style="visibility:hidden;" onload="this.style.visibility = \'visible\';"=></iframe>';
    jQuery('.modal-close').css({"display": "none", "top": "12px", 'right': '39px'});
    jQuery('#modal-content').html(html).css({'top': '-2000px', 'position': 'relative'});
    jQuery('#modal-window').append(jQuery("#preload-gif").html());
    jQuery('#modal-window img:last').css({'top': '47%', 'left': '47%', 'position': 'fixed'});

    jQuery('iframe#modal-iframe').load(function() {
        jQuery('#modal-content').css({"top": "0", 'position': 'relative'});
        jQuery('#modal-window img:last').remove();
        jQuery('.modal-close').css({"display": "block", "top": "12px", 'right': '39px'});
    });

    Disney.Play.modal.open(null, null, Disney.Play.closeModalCallback);

  };
  
  Disney.Play.closeModalCallback = function() {
    if (Disney.Play.newName) {
      try {
        $("#club_penguin")[0].handleNameResubmit(Disney.Play.newName, Disney.Play.newToken, Disney.Play.newLoginData);
      } catch(e){
        //console.log(e.message);
      }
    }
  }

  Disney.Play.setTrialBanner = function(responseText, textStatus, XMLHttpRequest) {										
    $('#affiliateheaderforcp').height(28);
    $('#club_penguin').height('95%');
    $('#hdrWrap').attr("style", "height:28px !important");
    
    if(Disney.Play.daysLeft > 1) {								
      var countDown = $('#TrialText').html().replace('%CountDown', daysLeft);
      $('#TrialText').html(countDown);	
      
      $('#TrialText2').remove();		
    } else  {
      $('#TrialText').remove();
    }
    
    if ($.browser.msie  && parseInt($.browser.version, 10) === 7) {
      $('#BannerContainer').height(28);
    } else {
      $('#BannerContainer').animate({height:'+28'}, 1000);
    }
  }	

  Disney.Play.setMembershipBanner = function(responseText, textStatus, XMLHttpRequest) {										
    $('#affiliateheaderforcp').height(28);
    $('#club_penguin').height('95%');
    $('#hdrWrap').attr("style", "height:28px !important");
    
    if(Disney.Play.daysLeft > 1) {								
      var countDown = $('#membership-banner-days').html().replace('%CountDown', Disney.Play.daysLeft);
      $('#membership-banner-days').html(countDown);	
      
      $('#membership-banner-day').remove();		
    } else {
      $('#membership-banner-days').remove();		
    }
    
    if ($.browser.msie  && parseInt($.browser.version, 10) === 7) {
      $('#BannerContainer').height(28);
    } else {
      $('#BannerContainer').animate({height:'+28'}, 1000);
    }
  }	

  Disney.Play.setActivateBanner = function(responseText, textStatus, XMLHttpRequest) {
    $('#affiliateheaderforcp').height(28);
    $('#club_penguin').height('95%');
    $('#hdrWrap').attr("style", "height:28px !important");
    
    if(Disney.Play.daysLeft > 1) {								
      var countDown = $('#pre-activated-banner-days').html().replace('%CountDown', Disney.Play.daysLeft);
      $('#pre-activated-banner-days').html(countDown);	
      
      $('#pre-activated-banner-hours').remove();		
      $('#pre-activated-banner-hour').remove();		
    } else if(Disney.Play.hoursLeft > 1) {
      var countDown = $('#pre-activated-banner-hours').html().replace('%CountDown', Disney.Play.hoursLeft);
      $('#pre-activated-banner-hours').html(countDown);	
      
      $('#pre-activated-banner-days').remove();		
      $('#pre-activated-banner-hour').remove();		
    } else {
      $('#pre-activated-banner-hours').remove();		
      $('#pre-activated-banner-days').remove();		
    }
    
    if ($.browser.msie  && parseInt($.browser.version, 10) === 7) {
      $('#BannerContainer').height(28);
    } else {
      $('#BannerContainer').animate({height:'+28'}, 1000);
    }
  }	

  Disney.Play.initLanguage = function() {
    var currentURL = window.location.pathname;
    var pathArray = currentURL.split("/");
    var langPath = pathArray[1];
    if ((langPath != "es") && (langPath != "fr") && (langPath != "pt") && (langPath != "de") && (langPath != "ru")) { langPath="" } 
    Disney.Play.langPath = (langPath == "" ? langPath : langPath + "/");
  }

  Disney.Play.addTracking = function(transActivityId, transRevenue, transOrderId, transProductId, transProductInfo) {
    // generate random #
    var trackingRand = Math.random()+'';
    trackingRand = trackingRand * 1000000;
    // Append the tracking code to document
    var imgSrc = 'HTTPS://bs.serving-sys.com/BurstingPipe/ActivityServer.bs?cn=as&amp;ActivityID='+ transActivityId + '&amp;Value='+ transRevenue + '&amp;OrderID='+ transOrderId + '&amp;ProductID='+ transProductId + '&amp;ProductInfo='+ transProductInfo +'&amp;ns=1&amp;rnd='+ trackingRand;
    $('body').append('<img width="1" height="1" style="border:0" src="'+ imgSrc +'" />');
  }

  Disney.Play.initTracking = function() {
    try {
      // MediaMind tracking for UK Campaign
      var transActivityId = '158291';
      var transRevenue = '';
      var transProductId = window.metrics.options.TRANSID;
      var transProductInfo = '';
      // add tracking to page
      Disney.Play.addTracking(transActivityId, transRevenue, '', transProductId, transProductInfo);
    } catch (e) {}
  }
  
  $("#BannerContainer").delegate("#pre-activated-banner-btn", "click", function(event) {
		window.metrics.log('game_action', {'context':'pre_activated_player', 'action':'about_activation_banner'});
		$("#club_penguin")[0].handleShowPreactivation();
	});	
	
  $("#BannerContainer").delegate("#TrialBannerLink", "click", function(event) {
    window.metrics.log('game_action', {'context':'membership_trial', 'action':'about_banner'});
	});	
	
	/* Change the big screen / small screen button to use javascript instead of reloading the page
	 * To prevent users from losing their session if the want to change to small screen mode
	 */

	$("#bigscreen a").click(function() {
		Disney.Play.setBigScreen();
		return false;
	});	
	$("#smallscreen a").click(function() {
		Disney.Play.setSmallScreen();
		return false;
	});	

	/* Force clean up of the flash object during logoff or if the user closes the window */
	$('a').click(function() {
		// only handle logoff when the link will leave the page.
		if ($(this).attr("href").search(/#/) < 0) {
			var cpMovie = document.getElementById("club_penguin");
			cpMovie.handleLogOff($(this).attr("href"));
			Disney.Play.flashCleanupNeeded = false;
			return false;
		}
	});

	$(window).unload(function() { 
		if (Disney.Play.flashCleanupNeeded) {
			var cpMovie = document.getElementById("club_penguin");
			cpMovie.handleWindowUnload();
		}
	});
	
	$(window).bind("hashchange",function(event) {
	    //If using back button to return to play.clubpenguin.com reload page
	    var newURL = event.originalEvent.newURL;
	    var oldURL = event.originalEvent.oldURL;
	    if (newURL.search("/#/") < 0 && oldURL.search("/#/") > 0) {
	      window.location.reload();
	    }
	});
	
	if (window.location.href.search(/smallscreen/) >= 0 ) {
		Disney.Play.setSmallScreen();
	} else {
		Disney.Play.setBigScreen();	
	}

  Disney.Play.newName = false;
  Disney.Play.newLoginData = false;
  Disney.Play.newToken = false;
  Disney.Play.flashCleanupNeeded = true;
  Disney.Play.initModal();
  Disney.Play.initLanguage();
  	
});
