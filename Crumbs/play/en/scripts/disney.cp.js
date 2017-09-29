//To allow cross sub domain scripting
document.domain = 'clubpenguin.com';
var Disney = Disney || {};
Disney.Play = Disney.Play || {};
Disney.Membership = Disney.Play; //Alias used by lightbox close

/* ExternalInterface Functions called from Club Penguin client
-----------------------------------------------------------------*/
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
                        window.metrics.testImpression("MembershipBanner", (result.membership_banner.isControl ? 1 : 0), result.membership_banner.variantIndex);
                      }
                    }
                });  
}

function TrialBannerLink() {
    window.metrics.log('game_action', {'context':'membership_trial', 'action':'about_banner'});
}

// Successful creation of a Penguin
function penguinCreateSuccessCallback(swid) {
    // Record successful Penguin creation in BI -- use SWID as userid and record under CP network
    override_options = {
			"SWID" : swid,
			"USERID" : swid,
			"NETWORK" : 'c',
			"VIEW_NETWORK" : 'cp',
		};
    swid_metrics = new CP.metrics(override_options);
    swid_metrics.game_action("success", "register");
  
    // MediaMind tracking for UK Campaign
    var cpMM_id = getCookie('cpMM');
    if (cpMM_id != null) {
        try {
            Disney.Play.initTracking(cpMM_id, swid);
        } catch(e){}
    }
    // MediaMind tracking for French
    // var cpMMFr_id = getCookie('cpMM_Fr');
    // if (cpMMFr_id != null) {
    //     try {
    //         Disney.Play.initTracking(cpMMFr_id, swid);
    //     } catch(e){}
    // }
    
}


/* Definitions
-----------------------------------------------------------------*/
(function($){

    /* Disney CP
    -------------------------------------------------*/
    Disney.CP = function(){
        this.currentIndex = 0;
    };

    Disney.CP.prototype.showRules = function(lang) {
        var self = this;
        $('#modal-content').load('rules-overlay.html #rules-wrap', function(){
            //open modal
            Disney.Play.modal.showClose = true;
            Disney.Play.modal.open('', 
                function(){ self.initRules(); }, 
                function(){ clearInterval(self.rulesInterval); }
            );
        });
    };

    Disney.CP.prototype.setTimer = function(currentIndex) {
        var self = this;
        self.rulesInterval = setInterval(function(){
            self.currentIndex = (self.currentIndex+1) % $("#rules ul li").length;
            self.showRule(self.currentIndex);
        }, 5000);
    };

    Disney.CP.prototype.initRules = function(){
        var self = this;
        if ($("#rules").length > 0) {
            $("#rules ul li").mouseover(function(){
                self.currentIndex = $("#rules ul li").index(this);
                self.showRule(self.currentIndex);
            });

            $("#rules ul li").mouseenter(function(){
                clearInterval(self.rulesInterval);
            }).mouseleave(function(){
                self.currentIndex = $("#rules ul li").index(this);
                self.setTimer(self.currentIndex);
            });

            self.setTimer(0);
        }
    };

    Disney.CP.prototype.showRule = function(index) {
        $("#rules ul li").removeClass("active");
        $($("#rules ul li")[index]).addClass("active");
        $("#rules-container").html( $($("#rules ul li")[index]).html());
    };

    /* Disney Play
    -------------------------------------------------*/
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
        } catch(e){}
    };

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
        } catch(e){}
    };

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
    };

    Disney.Play.stopEvent = function(event) {
        if (event.cancelable) {
            event.preventDefault();
        }
        event.cancelBubble = true;
        if (event.stopPropagation) {
            event.stopPropagation();
        }
    };

    Disney.Play.initModal = function() {
        Disney.Play.modal = new CP.utils.Modal({
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

        Disney.Play.modal.showClose = false;
        Disney.Play.modal.open(null, null, Disney.Play.closeModalCallback);
    };
  
    Disney.Play.closeModalCallback = function() {
        if (Disney.Play.newName) {
            try {
                $("#club_penguin")[0].handleNameResubmit(Disney.Play.newName, Disney.Play.newToken, Disney.Play.newLoginData);
            } catch(e){}
        }
    };

    Disney.Play.setTrialBanner = function(responseText, textStatus, XMLHttpRequest) { 
        $('#affiliateheaderforcp').height(28);
        $('#club_penguin').height('95%');
        $('#hdrWrap').attr("style", "height:28px !important");

        if(Disney.Play.daysLeft > 1) {                              
            var countDown = $('#TrialText').html().replace('%CountDown', Disney.Play.daysLeft);
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
    }; 

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
    };

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
    };

    Disney.Play.initLanguage = function() {
        var currentURL = window.location.pathname;
        var pathArray = currentURL.split("/");
        var langPath = pathArray[1];
        if ((langPath != "es") && (langPath != "fr") && (langPath != "pt") && (langPath != "de") && (langPath != "ru")) { langPath="" } 
        Disney.Play.langPath = (langPath == "" ? langPath : langPath + "/");
    };

    Disney.Play.addTracking = function(transActivityId, transRevenue, transOrderId, transProductId, transProductInfo) {
        // generate random #
        var trackingRand = Math.random()+'';
        trackingRand = trackingRand * 1000000;
        // Append the tracking code to document
        var imgSrc = 'HTTPS://bs.serving-sys.com/BurstingPipe/ActivityServer.bs?cn=as&amp;ActivityID='+ transActivityId + '&amp;Value='+ transRevenue + '&amp;OrderID='+ transOrderId + '&amp;ProductID='+ transProductId + '&amp;ProductInfo='+ transProductInfo +'&amp;ns=1&amp;rnd='+ trackingRand;
        $('body').append('<img width="1" height="1" style="border:0" src="'+ imgSrc +'" />');
    };

    Disney.Play.initTracking = function(activityId, swid) {
        try {
            // MediaMind tracking
            var transActivityId = activityId;
            var transRevenue = '';
            var transProductId = window.metrics.options.TRANSID;
            var transProductInfo = '';
            // add tracking to page
            Disney.Play.addTracking(transActivityId, transRevenue, swid, transProductId, transProductInfo);
        } catch(e){}
    };
    
    Disney.Play.get_browser = function() {
        var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []; 
        if(/trident/i.test(M[1])){
            tem=/\brv[ :]+(\d+)/g.exec(ua) || []; 
            return 'IE '+(tem[1]||'');
            }   
        if(M[1]==='Chrome'){
            tem=ua.match(/\bOPR\/(\d+)/)
            if(tem!=null)   {return 'Opera '+tem[1];}
            }   
        M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
        if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
        return M[0];
    }

    Disney.Play.get_browser_version = function() {
        var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];                                                                                                                         
        if(/trident/i.test(M[1])){
            tem=/\brv[ :]+(\d+)/g.exec(ua) || [];
            return 'IE '+(tem[1]||'');
            }
        if(M[1]==='Chrome'){
            tem=ua.match(/\bOPR\/(\d+)/)
            if(tem!=null)   {return 'Opera '+tem[1];}
            }   
        M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
        if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
        return M[1];
    }    
    
    

})(window.jQuery);



/* Document ready
-----------------------------------------------------------------*/
window.jQuery(document).ready(function(e){
    window.cp = new Disney.CP();
    //// Initializations
    Disney.Play.newName = false;
    Disney.Play.newLoginData = false;
    Disney.Play.newToken = false;
    Disney.Play.flashCleanupNeeded = true;
    Disney.Play.initModal();
    Disney.Play.initLanguage();
 
    //// Banner Events
    $("#BannerContainer").delegate("#pre-activated-banner-btn", "click", function(event) {
        window.metrics.log('game_action', {'context':'pre_activated_player', 'action':'about_activation_banner'});
        $("#club_penguin")[0].handleShowPreactivation();
    });	
    $("#BannerContainer").delegate("#TrialBannerLink", "click", function(event) {
        window.metrics.log('game_action', {'context':'membership_trial', 'action':'about_banner'});
    });
  
    //// Flash Upgrade Message Button tracking
    $("#upgrade #ignoreButton a").click(function() {
        window.metrics.log('game_action', {'context':'upgrade_message', 'action':'no_thanks'});
    });
	
    $("#upgrade #upgradeButton a").click(function() {
        window.metrics.log('game_action', {'context':'upgrade_message', 'action':'upgrade_now'});
    });
	
    //// Big Screen, Small Screen
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

    //// Window Unload
    $(window).unload(function() { 
        if (Disney.Play.flashCleanupNeeded) {
            var cpMovie = document.getElementById("club_penguin");
            cpMovie.handleWindowUnload();
        }
    });

    //// Hash Change Binding
    $(window).bind("hashchange",function(event) {
        //If using back button to return to play.clubpenguin.com reload page
        var newURL = event.originalEvent.newURL;
        var oldURL = event.originalEvent.oldURL;
        if (newURL.search("/#/") < 0 && oldURL.search("/#/") > 0) {
            window.location.reload();
        }
        if (newURL.search(/create/) >= 0) {
            newHostname = location.hostname.replace("play","secured");
            newProtocol = ((newHostname.indexOf("sandbox") >= 0) ? "http" : "https");
            window.location.href = newProtocol + "://" + newHostname + "/" + Disney.Play.langPath + "penguin/create";
        }
    });
    
    //// Redirect Creates to new version
    if (window.location.href.search(/create/) >= 0) {
        newHostname = location.hostname.replace("play","secured");
        newProtocol = ((newHostname.indexOf("sandbox") >= 0) ? "http" : "https");
        window.location.href = newProtocol + "://" + newHostname + "/" + Disney.Play.langPath + "penguin/create";
    }
	
    //// Small Screen Check
	if (window.location.href.search(/smallscreen/) >= 0 ) {
		Disney.Play.setSmallScreen();
	} else {
		Disney.Play.setBigScreen();	
	}

    //// BI
    var userid = getCookie('playspanSWID');
    if( userid !== null && userid !== "-1"){
        window.metrics.network_mapping_info();
    }
    window.metrics.clickedLink();
    var url = window.location.pathname;
    window.metrics.pageView(url);
    try {
        if ($('.abtest').length > 0) {
            $('.abtest').each(function(i, occurrence){
                var testName = $(this).attr('rel');
                var testType = $(this).children().get(0).className;
                var control = 1;
                var variant = 0;
                if (testType != 'control') {
                    variant = testType.replace('variant', '');
                    control = 0;
                }
                window.metrics.testImpression(testName, control, variant);
            });
        }
    } catch(e){}
});
