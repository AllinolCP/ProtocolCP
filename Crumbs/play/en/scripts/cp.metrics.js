if (typeof CP === 'undefined') {
	var CP = {};
}

(function($) {

	CP.metrics = function(options) {
		var hostName = window.location.hostname, swid, prefix;
		this.initOptions();
		$.extend(true, this.options, options);

		// -- Referrer
		this.options.REF = document.referrer;

		// -- TransID
		if (this.options.TRANSID === '-1') {
			transid = getCookie('playspanTRANSID');
		}
		if (transid && transid !== "null") {
			this.options.TRANSID = transid;
		}
		if (this.options.TRANSID === '-1' || this.options.TRANSID === "null") {
			// If we still have '-1' or "null" assign unique identifier
			// Generate a GUID
			transid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) { var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8); return v.toString(16); });
			this.options.TRANSID = transid;
			try {
				setCookie('playspanTRANSID', transid);
			} catch(e){}
		}

		// -- BrowserID
		if (this.options.BROWSERID === '-1') {
			browserid = getCookie('cpBROWSERID');
		}
		if (browserid && browserid !== "null") {
			this.options.BROWSERID = browserid;
		}
		if (this.options.BROWSERID === '-1' || this.options.BROWSERID === "null") {
			// If we still have '-1' or "null" assign unique identifier
			//Generate a GUID
			browserid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) { var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8); return v.toString(16); });
			this.options.BROWSERID = browserid;
			try {
				setCookie('cpBROWSERID', browserid, 365);
			} catch (e){}
		}

		// -- SWID
		if (this.options.SWID === '-1') {
			swid = getCookie('playspanSWID');
		}
		if (swid && swid !== "null") {
			this.options.SWID = swid;
		}

		// -- UserID
		if (this.options.USERID === '-1') {
		  if (this.options.VIEW_NETWORK == 'cp' && this.options.SWID != '-1') {
		    this.options.USERID = this.options.SWID;
		  } else {
		    this.options.VIEW_NETWORK = 'bd'
		    this.options.USERID = this.options.BROWSERID;
		  }
		}

		// -- App Name & Context
		if (!this.options.CONTEXT_PREFIX) {
			prefix = getCookie('contextVariant') || 'purchase_funnel_';
			this.setContextVariant(prefix);
		}
		if (hostName.indexOf("stage") >= 0 || hostName.indexOf("localhost") >= 0 || hostName.indexOf("sandbox") >= 0 || hostName.indexOf("qa") >= 0 || hostName.indexOf("dev") >= 0) {
			this.options.API_APP_NAME = "qa_" + this.options.API_APP_NAME;
		}

		// -- App Locale
		if (document.documentElement.lang) {
			this.options.APP_LOCALE = document.documentElement.lang.toLowerCase().substr(0, 2);
		}
		switch (this.options.APP_LOCALE) {
			case "en":
				this.options.APP_LOCALE += "_US";
				break;
			case "pt":
				this.options.APP_LOCALE += "_BR";
				break;
			case "fr":
				this.options.APP_LOCALE += "_FR";
				break;
			case "es":
				this.options.APP_LOCALE += "_ES";
				break;
			case "de":
				this.options.APP_LOCALE += "_DE";
				break;
			case "ru":
				this.options.APP_LOCALE += "_RU";
				break;
		}
	};

	CP.metrics.prototype.setSWID = function(swid) {
		if (swid && swid !== "null") {
			this.options.SWID = swid;
			try {
				setCookie('playspanSWID', swid);
				window.metrics.network_mapping_info();
			} catch (e) {
			}
		}
	};

	CP.metrics.prototype.getTRANSID = function() {
		if (transid && transid !== "null") {
			return transid;
		}
	};

	CP.metrics.prototype.setContextVariant = function(variant) {
		this.options.CONTEXT_PREFIX = variant;
		try {
			setCookie('contextVariant', variant);
		} catch (e) {
		}
	};

	CP.metrics.prototype.logTimingEvent = function(location, moreData) {
		var tag = this.options.TAG, network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE, context = this.options.CONTEXT, transid = this.options.TRANSID, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'lang' : appLocale,
			'app_locale' : appLocale,
			'context' : context,
			'location' : location,
			'timestamp_ms' : (new Date()).getTime(),
			'transaction_id' : transid,
			'browser_id' : browserid,
			'abTestId' : browserid
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}

		this.logEvent(data);
	};

	CP.metrics.prototype.logError = function(moreData) {
		var tag = 'error', network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'lang' : appLocale,
			'app_locale' : appLocale,
			'browser_width' : $(window).width(),
			'browser_height' : $(window).height()
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}
		this.logEvent(data);
	};

	CP.metrics.prototype.pageView = function(page, moreData) {

		if(window.location.hostname.indexOf("play") >= 0){
			page = "play";
		}

		var tag = 'pageview', network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE
		, transid = this.options.TRANSID, browserid = this.options.BROWSERID, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'lang' : appLocale,
			'app_locale' : appLocale,
			'transaction_id' : transid,
			'browser_id' : browserid,
			'location' : page,
			'browser_width' : $(window).width(),
			'browser_height' : $(window).height(),
			'abTestId' : browserid
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}
		this.logEvent(data);
	};

	CP.metrics.prototype.network_mapping_info = function(moreData) {
		this.options.VIEW_NETWORK = "bd";
		var secondarynetwork = "cp";
		var tag = 'network_mapping_info', network = this.options.NETWORK, viewNetwork=this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE
		, browserid = this.options.BROWSERID, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'app_locale' : appLocale,
			'secondary_user_id' : this.options.SWID,
			'secondary_network' : secondarynetwork
		};

		if (moreData) {
			$.extend(true, data, moreData);
		}

		var networkMappingSent = getCookie('networkMappingSent') || 0;
		if (networkMappingSent == 0) {
			this.logEvent(data);
			setCookie('networkMappingSent', 1);
		}
	};

	CP.metrics.prototype.game_action = function(action, name, moreData) {
		var tag = 'game_action', network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE
		, transid = this.options.TRANSID, browserid = this.options.BROWSERID, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'lang' : appLocale,
			'app_locale' : appLocale,
			'transaction_id' : transid,
			'browser_id' : browserid,
			'context' : name,
			'action' : action
		};

		if (moreData) {
			$.extend(true, data, moreData);
		}

		this.logEvent(data);
	};

	CP.metrics.prototype.testImpression = function(testName, control, variant) {
		var tag = 'test_impression', network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE
		var url = window.location.pathname, transid = this.options.TRANSID, browserid = this.options.BROWSERID, Swid = this.options.SWID, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'app_locale' : appLocale,
			'browser_id' : browserid,
			'SWID' : Swid,
			'test' : testName,
			'control' : control,
			'variant' : variant
		};
		this.logTestImpression(data);
	};

	CP.metrics.prototype.clickedLink = function(moreData) {
		//Only log this if referrer is not *.clubpenguin.com
		var referrerUrl = '';
		if (this.options.REF) {
			 referrerUrl =  this.options.REF;
		}

		//Grab the original homepage referrer because we force a redirect for geo targetting purposes.
		homepageReferrer = getCookie('homepageReferrer');
		if (homepageReferrer && homepageReferrer !== "null") {
		  referrerUrl =  homepageReferrer;
		  //clear the cookie value
		  setCookie('homepageReferrer', 'null', -1);
		}

		var tag = 'clicked_link', network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE
		var trackingCodeCMP = this.getQueryParam('cmp'), trackingCodeOAST = this.getQueryParam('oast');
		var trackingCode = "";
		//only one or the other will be set cmp = emails, oast = banners etc
		if (trackingCodeCMP) {
			trackingCode += trackingCodeCMP;
		}
		if (trackingCodeOAST) {
			trackingCode += trackingCodeOAST;
		}
		var trackUrl = window.location.href, isNewUser = (getCookie('cpvisitor') == "new" ? 1 : 0 );
		var transid = this.options.TRANSID, browserid = this.options.BROWSERID, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'lang' : appLocale,
			'app_locale' : appLocale,
			'transaction_id' : transid,
			'browser_id' : browserid,
			'abTestId' : browserid,
			'is_new_user' : isNewUser,
			'tracking_code' : trackingCode,
			'ref_id' : "", //do not know what this is referring to.
			'track_url' : encodeURIComponent(trackUrl),
			'referrer_url' : encodeURIComponent(referrerUrl)
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}

		//log each clicked link
		if (referrerUrl != '') {
			var referrerUrlSplit = referrerUrl.split('/');
			//hostname will be in array value 2
			var referrerUrl = referrerUrlSplit[2];
			// DRTV Domains - since we're already past the point of setting the logging variable
			// this test is just so we ensure that NO logging occurs for DRTV Parents page when referrer is DRTV Kids
			// and Membership Purchase pages are NOT logged when coming from DRTV Parents
			if (referrerUrl.match(/clubpenguinoffer.com/) || referrerUrl.match(/clubpenguintv.com/) || referrerUrl.match(/getclubpenguin.com/) || referrerUrl.match(/tryclubpenguin.com/)) {
				referrerUrl = 'clubpenguin.com';
			}
		}
		if (!referrerUrl.match(/clubpenguin.com/) || trackingCode != "") {
			this.logEvent(data);
		}
	};

	CP.metrics.prototype.user_info = function(device_type, device_model, os_version, moreData) {
		var data = {
			'tag' : 'user_info',
			'network' : this.options.NETWORK,
			'view_network' : this.options.VIEW_NETWORK,
			'app_locale' : this.options.APP_LOCALE,
			'transaction_id' : this.options.TRANSID,
			'browser_id' : this.options.BROWSERID,
			'device_type' : device_type,
			'os_version' : os_version,
			'model' : device_model
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}
		this.logEvent(data);
	};

	CP.metrics.prototype.geo = function(moreData) {
		//Only log this if referrer is not *.clubpenguin.com
		var referrerUrl = '';
		if (this.options.REF) {
			 referrerUrl =  this.options.REF;
		}
		var data = {
			'tag' : 'geo',
			// 'useragent' : navigator.userAgent
			'network' : this.options.NETWORK,
			'view_network' : this.options.VIEW_NETWORK,
			'app_locale' : this.options.APP_LOCALE
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}

		//log each clicked link
		if (referrerUrl != '') {
			var referrerUrlSplit = referrerUrl.split('/');
			//hostname will be in array value 2
			var referrerUrl = referrerUrlSplit[2];
			// DRTV Domains - since we're already past the point of setting the logging variable
			// this test is just so we ensure that NO logging occurs for DRTV Parents page when referrer is DRTV Kids
			// and Membership Purchase pages are NOT logged when coming from DRTV Parents
			if (referrerUrl.match(/clubpenguinoffer.com/) || referrerUrl.match(/clubpenguintv.com/) || referrerUrl.match(/getclubpenguin.com/) || referrerUrl.match(/tryclubpenguin.com/)) {
				referrerUrl = 'clubpenguin.com';
			}
		}
		if (!referrerUrl.match(/clubpenguin.com/)) {
			var pic, url = window.location.protocol + "//log.data.disney.com/g?app=" + this.options.API_APP_NAME + "&user_id=" + this.options.USERID;
			for ( var key in data) {
				if (data.hasOwnProperty(key)) {
					url += "&" + key + "=" + data[key];
				}
			}
			url += '&rnd=' + Math.random();	// adding random to avoid img caching in FF
			if (this.callbackImage) {
				pic = this.callbackImage;
			} else {
				pic = new Image();
			}
			pic.src = url;
		}
	};

	CP.metrics.prototype.log = function(tag, moreData) {
		var transid = this.options.TRANSID;
		var network = this.options.NETWORK, viewNetwork = this.options.VIEW_NETWORK, appLocale = this.options.APP_LOCALE, data = {
			'tag' : tag,
			'network' : network,
			'view_network' : viewNetwork,
			'lang' : appLocale,
			'app_locale' : appLocale,
			'browser_width' : $(window).width(),
			'browser_height' : $(window).height(),
			'transaction_id' : transid
		};
		if (moreData) {
			$.extend(true, data, moreData);
		}
		this.logEvent(data);
	};

	CP.metrics.prototype.logEvent = function(data) {
		if (data) {
			$.extend(true, this.options, data);
		}
		var pic, url = window.location.protocol + "//log.data.disney.com/cp?app=" + this.options.API_APP_NAME + "&user_id=" + this.options.USERID;
		for ( var key in data) {
			if (data.hasOwnProperty(key)) {
				url += "&" + key + "=" + data[key];
			}
		}
		url += '&rnd=' + Math.random();	// adding random to avoid img caching in FF

		if (this.callbackImage) {
			pic = this.callbackImage;
		} else {
			pic = new Image();
		}
		pic.src = url;
	};

	CP.metrics.prototype.logTestImpression = function(data) {
		if (data) {
			$.extend(true, this.options, data);
		}
		var TI_APP_NAME ="clubpenguin";
		var hostName = window.location.hostname, swid, prefix;
		if (hostName.indexOf("stage") >= 0 || hostName.indexOf("sandbox") >= 0 || hostName.indexOf("qa") >= 0 || hostName.indexOf("dev") >= 0) {
			TI_APP_NAME = "qa_" + TI_APP_NAME;
		}

		var pic, url = window.location.protocol + "//log.data.disney.com/cp?app="+ TI_APP_NAME + "&user_id=" + this.options.BROWSERID;
		for ( var key in data) {
			if (data.hasOwnProperty(key)) {
				url += "&" + key + "=" + data[key];
			}
		}
		if (this.callbackImage) {
			pic = this.callbackImage;
		} else {
			pic = new Image();
		}
		pic.src = url;
	};

	CP.metrics.prototype.stepTime = function(funnelName, stepName, moreData) {
		this.options.TAG = 'step_timing';
		try {
			var existingFunnel = getCookie('playspanFunnelName');
			if (!this.options.CONTEXT) {
				this.options.CONTEXT = existingFunnel;
				if (!this.options.CONTEXT) {
					if (funnelName.indexOf('_') < 0) {
						funnelName = this.options.CONTEXT_PREFIX + funnelName;
					}
					setCookie('playspanFunnelName', funnelName);
					this.options.CONTEXT = funnelName;
				}
			}

			this.logTimingEvent(stepName, moreData);
			if (stepName === 'end') {
				this.reset();
			}
		} catch (e) {
		}
	};

	CP.metrics.prototype.reset = function() {
		this.initOptions();
		setCookie('playspanFunnelName', '');
		setCookie('contextVariant', '');
	};

	CP.metrics.prototype.initOptions = function() {
		this.options = {
			API_APP_NAME : 'clubpenguin',
			SWID : '-1',
			ABTESTID : '-1',
			TRANSID : '-1',
			BROWSERID : '-1',
			USERID : '-1',
			CONTEXT : '',
			APP_LOCALE : 'en_US',
			LOCALE : 'en_US',
			NETWORK : 'c',
			VIEW_NETWORK : 'bd',
			REASON : '',
			TAG : '',
			CONTEXT_PREFIX : ''
		};
	};

	CP.metrics.prototype.track = function(pagename) {
		try {
			cto.pageName = pagename;
			cto.track();
			return true;
		} catch (e) {
			return false;
		}
	};

	CP.metrics.prototype.getQueryParam = function(param) {
		//escape any regex dilimeters
		name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
		//find the param in the query string
	    var result =  window.location.search.match(
	        new RegExp("(\\?|&)" + param + "(\\[\\])?=([^&]*)")
	    );

	    //If found return value else return false;
	    return result ? result[3] : false;
	}

})(window.jQuery);

window.jQuery(document).ready(function($) {
	window.metrics = new CP.metrics();
});
