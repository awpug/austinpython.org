(function() {

  var TWITTER_BASE = "http://search.twitter.com/search.json";
  var MAX_RESULTS = 10;

  var formatDate = function(date) {
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();
    var minute = date.getMinutes();
    var hour = date.getHours() + 1;
    var meridian = "am";
    if (hour > 12) {
      hour = hour - 12;
      meridian = "pm";
    }
    return hour+":"+minute+meridian+" on "+month+"/"+day+"/"+year;
  };

  var getTweetEl = function(text) {
    var tweetEl = jQuery("<p class='tweet-text'></p>");
    var cleanContent = tweetEl.text(text).html(); // escape content
    cleanContent = cleanContent.replace(/(http:\/\/[\w\_\?\=\-\/\#\!\+\.]+)/ig, "<a href='$1' target='_blank'>$1</a>");
    cleanContent = cleanContent.replace(/@([\w\_]+)/ig, "<a href='http://twitter.com/$1' target='_blank'>@$1</a>");
    return tweetEl.html(cleanContent);
  };

  var TwitterSearch = function(config) {
    this._config = config;
    this._maxResults = config.results || MAX_RESULTS;
    this._container = jQuery(config.container);
    this._id = "T"+Math.round(Math.random()*1000000);
    this._tweetClassName = this._config.className;
    window.twitterSearch.register[this._id] = this;
  };

  TwitterSearch.prototype.init = function() {
    // starts the search, fetches the tweets
    var params = {
      q: this._config.query,
      callback: "window.twitterSearch.register."+this._id+".update"
    };
    var paramString = "";
    for (var paramName in params) {
      if (params.hasOwnProperty(paramName)) {
        if (paramString.length) {
          paramString += "&";
        }
        paramString += paramName+"="+encodeURIComponent(params[paramName]);
      }
    }
    var searchUrl = TWITTER_BASE + "?" + paramString;
    var el = jQuery("<script type='text/javascript' src='"+searchUrl+"'></script>");
    jQuery("body").append(el);
  };

  TwitterSearch.prototype.update = function(tweets) {
    var results = tweets.results;
    if (results) {
      this._container.empty();
      for (var i=0; i<results.length && i<this._maxResults; i++) {
        // should replace this with underscore / etc. templates
        var tweet = results[i];
        var tweetEl = jQuery("<li class='tweet'></li>");
        if (this._tweetClassName) {
          tweetEl.addClass(this._tweetClassName);
        }
        tweetEl.append("<img src='"+tweet.profile_image_url+"' class='twitter-avatar'/>");
        tweetEl.append("<h3><a href='http://twitter.com/"+tweet.from_user+"'>"+tweet.from_user_name+"</a></h3>");
        tweetEl.append(getTweetEl(tweet.text));
        var tweetDate = new Date(tweet.created_at);
        tweetEl.append("<p class='tweet-info'>tweeted "+formatDate(tweetDate)+"</p>");
        this._container.append(tweetEl);
      }
    }
  };

  window.twitterSearch = {
    TwitterSearch: TwitterSearch,
    register: {}
  };

})();
