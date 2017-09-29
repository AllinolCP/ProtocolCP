//Name Resubmission has nothing to do with membership but shares several js functions/classes with membership/login so hence the name.
//To allow cross sub domain scripting
document.domain = 'clubpenguin.com';
var Disney = Disney || {};

jQuery(document).ready(function() {
  Disney.Membership = Disney.Membership || {};

  Disney.Membership.initModal = function() {
    jQuery("#modal-overlay").remove();
    jQuery("#modal-loading").remove();
    jQuery("#modal-window").remove();

    Disney.Membership.modal = new CP.utils.Modal({
      showClose: false,
      overlayClickClose: false, //too easy to accidentally close the lightbox with no way to reopen.
      contentCloseDelegate: '.modal-close',
      onOpenComplete: function() {},
      onCloseComplete: function() {},
      onCloseStart: function() {},
      onOpenStart: function() {}
    });
    jQuery('.modal-close').css({"display": "none", "top": "12px", 'right': '39px'});
  };

  Disney.Membership.showModal = function(url) {
    var rdm = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) { var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8); return v.toString(16); });
    html = '<iframe id="modal-iframe" src="'+url+'?'+rdm+'" height="500" width="500" allowtransparency="true" marginheight="0" marginwidth="0" frameborder="0" style="overflow:hidden;" style="visibility:hidden;" onload="this.style.visibility = \'visible\';"=></iframe>';
    jQuery('#modal-content').html(html).css({'top': '-2000px', 'position': 'relative'});
    jQuery('#modal-window').append(jQuery("#preload-gif").html());
    jQuery('#modal-window img:last').css({'top': '47%', 'left': '47%', 'position': 'fixed'});

    jQuery('iframe#modal-iframe').load(function() {
        jQuery('#modal-content').css({"top": "0", 'position': 'relative'});
        jQuery('#modal-window img:last').remove();
        jQuery('.modal-close').css({"display": "block", "top": "12px", 'right': '39px'});
    });

    Disney.Membership.modal.open(null, null, Disney.Membership.closeModalCallback);

  };

  Disney.Membership.initLanguage = function() {
    var currentURL = window.location.pathname;
    var pathArray = currentURL.split("/");
    var langPath = pathArray[1];
    if ((langPath != "es") && (langPath != "fr") && (langPath != "pt") && (langPath != "de") && (langPath != "ru")) { langPath="" } 
    Disney.Membership.langPath = (langPath == "" ? langPath : langPath + "/");
  }
  
  Disney.Membership.closeModalCallback = function() {
    if (Disney.Membership.newName) {
      try {
        $("#club_penguin")[0].handleNameResubmit(Disney.Membership.newName, Disney.Membership.newToken, Disney.Membership.newLoginData);
      } catch(e){
        //console.log(e.message);
      }
    }
  }

  Disney.Membership.newName = false;
  Disney.Membership.newLoginData = false;
  Disney.Membership.newToken = false;
  Disney.Membership.initModal();
  Disney.Membership.initLanguage();
});

function nameResubmission(player_id, token, data) {
  newHostname = location.hostname.replace("play","secured");
  newProtocol = ((newHostname.indexOf("sandbox") >= 0) ? "http:" : "https:");
  var href = newProtocol + "//" + newHostname + "/" + Disney.Membership.langPath + "penguin/update-username/" + player_id + "/" + token + "/" + data;
  Disney.Membership.showModal(href);
};




