// register the plugin within the editor
(function() {
    var flashFilenameRegex = /\.swf(?:$|\?)/i;

    function isFlashEmbed( element ) {
	var attributes = element.attributes;
        
	return ( attributes.type == 'application/x-shockwave-flash' || flashFilenameRegex.test( attributes.src || '' ) );
    }
    
    function createFakeElement( editor, realElement ) {
	return editor.createFakeParserElement( realElement, 'cke_youtube', 'flash', true );
    }
    
    CKEDITOR.plugins.add('youtube', {
        
        // register the icons
        icons: 'youtube',
        
        onLoad: function() {
            CKEDITOR.addCss('img.cke_youtube' + 
                            '{' +
                            'background-image: url(' + 
                            CKEDITOR.getUrl(this.path + 
                                            'images/placeholder.png' ) + ');' +
			    'background-position: center center;' +
			    'background-repeat: no-repeat;' +
			    'border: 1px solid #a9a9a9;' +
			    'width: 80px;' +
			    'height: 80px;' +
			    '}'
                           );
        }, // end onLoad
        
        // the plugin initialization logic goes inside this method.
        init: function(editor) {
            
            // define an editor command that opens our dialog.
            editor.addCommand('youtube',
                              new CKEDITOR.dialogCommand('youtubeDialog'));
            
            // create a toolbar button that executes the above command.
            editor.ui.addButton('youtube', {
                
                // the text part of the button (if available) and tooltip
                label: 'Insert Youtube Video',
                
                // the command to execute on click
                command: 'youtube',
                
                // the button placement in the toolbar (toolbar group name)
                toolbar: 'insert'
            });
            
            // register dialog file. this.path is the plugin folder path
            CKEDITOR.dialog.add('youtubeDialog',
                                this.path + 'dialogs/youtube.js');
            
            
            editor.on( 'doubleclick', function( evt ) {
		var element = evt.data.element;
                if (element.is('img') && 
                    element.data('cke-real-element-type') == 'flash')
		    evt.data.dialog = 'youtubeDialog';
	    });
            
            // If the "contextmenu" plugin is loaded, register the listeners.
	    if (editor.contextMenu ) {
                editor.addMenuGroup( 'youtubeGroup' );
                editor.addMenuItem( 'youtubeItem', {
                    label: 'Edit Youtube Video',
                    icon: this.path + 'icons/youtube.png',
                    command: 'youtube',
                    group: 'youtubeGroup'
                });
                
		editor.contextMenu.addListener( function( element) {
		    if (element.is('img') && 
                        element.data('cke-real-element-type') == 'flash')
                        return {youtubeItem : CKEDITOR.TRISTATE_OFF};
		});
	    }
            
        }, // end init
        
        afterInit: function( editor ) {
	    var dataProcessor = editor.dataProcessor,
	    dataFilter = dataProcessor && dataProcessor.dataFilter;
            
	    if ( dataFilter ) {
		dataFilter.addRules({
		    elements: {
			'cke:object': function( element ) {
			    var attributes = element.attributes,
			    classId = attributes.classid && String(
                                attributes.classid ).toLowerCase();
                            
			    if ( !classId && !isFlashEmbed( element ) ) {
				// Look for the inner <embed>
				for (var i=0; i<element.children.length; i++ ) {
				    if (element.children[i].name=='cke:embed') {
					if (!isFlashEmbed(element.children[i]))
					    return null;
                                        
					return createFakeElement(editor,
                                                                 element);
				    }
				}
				return null;
			    }
                            
			    return createFakeElement( editor, element );
			},
                        
			'cke:embed': function( element ) {
			    if ( !isFlashEmbed( element ) )
				return null;
                            
			    return createFakeElement( editor, element );
			}
		    }
		}, 5 );
	    }
	} // end afterInit
        
    });
})();