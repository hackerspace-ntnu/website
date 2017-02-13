/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    config.stylesSet = [];
    config.height = '100%'
};


CKEDITOR.on('instanceReady', function( ev ) {
  ev.editor.dataProcessor.htmlFilter.addRules({
    elements: {
      p: function (e) { e.attributes.class = 'flow-text'; },
      li: function (e) { e.attributes.class = 'flow-text'; }
    },
  });
});
