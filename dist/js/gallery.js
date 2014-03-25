/*var images = [
  {
    image: 'http://placehold.it/800x400',
    title: 'My cool title',
    description: 'My cool description'
  },
  {
    image: 'http://placehold.it/800x400',
  },
  {
    image: 'http://placehold.it/800x400',
  },
  {
    image: 'http://placehold.it/800x400',
  }
];*/

$(document).ready(function(){
  /* Run gallery */
  Galleria.run('.galleria', {
    //dataSource: images,
    flickr: 'set:72157642546421854',
    flickrOptions: {
      description: true,
    },
    transitionSpeed: 100,
  });
  Galleria.loadTheme('./dist/js/galleria/themes/classic/galleria.classic.min.js');
});
