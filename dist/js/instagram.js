$(document).ready(function() {
  var feed = new Instafeed({
    get: 'tagged',
    tagName: 'hackerspacentnu',
    clientId: 'a287cbc7f0794cfaad6fce4908f4a333',
    limit: 6,
    template: '<div class="col-md-2 col-xs-4"><a href="{{link}}"><img class="img-thumbnail" src="{{image}}" /></a></div>'
  });
  feed.run();
});
