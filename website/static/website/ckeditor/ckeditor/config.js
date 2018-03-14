/**
 *  * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 *   * For licensing, see LICENSE.md or http://ckeditor.com/license
 *    */

CKEDITOR.editorConfig = function( config ) {
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.stylesSet = [];
	config.height = '100%';
	config.coreStyles_bold = { element: 'b', overrides: 'strong' };
};


CKEDITOR.on('instanceReady', function( ev ) {
	ev.editor.dataProcessor.htmlFilter.addRules({
		elements: {
			p: function (e) { 
					e.attributes.class = 'test';
			},
			ul: function (e) { e.attributes.class = 'article-ul'; }
		},
	});
});
