$(document).ready(function () {
    /* Run gallery */
    Galleria.run('.galleria', {
        //dataSource: images,
        flickr: 'set:72157642546421854',
        show: 11,
        flickrOptions: {
            description: true
        },
        transitionSpeed: 100
    });
    Galleria.loadTheme('./dist/js/galleria/themes/classic/galleria.classic.min.js');
});
