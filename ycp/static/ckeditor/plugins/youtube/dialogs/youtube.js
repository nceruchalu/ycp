//(function() {
// Map 'true' and 'false' values to match W3C's specifications
// http://www.w3.org/TR/REC-html40/present/frames.html#h-16.5
var checkboxValues = {
    controls: { 'true': '1', 'false': '0' },
    rel: { 'true': '1', 'false': '0' },
    showinfo:{ 'true': '1', 'false': '0' },
    theme:{'true':'dark', 'false':'light'}
};

function loadValue( iframeNode ) {
    var isCheckbox = this instanceof CKEDITOR.ui.dialog.checkbox;
    if ( iframeNode.hasAttribute( this.id ) ) {
	var value = iframeNode.getAttribute( this.id );
	if ( isCheckbox )
	    this.setValue( checkboxValues[this.id ][ 'true' ] ==
                           value.toLowerCase() );
	else
	    this.setValue( value );
    }
}

function commitValue( iframeNode ) {
    var isRemove = this.getValue() === '',
    isCheckbox = this instanceof CKEDITOR.ui.dialog.checkbox,
    value = this.getValue();
    if ( isRemove )
	iframeNode.removeAttribute( this.att || this.id );
    else if ( isCheckbox )
	iframeNode.setAttribute( this.id, checkboxValues[this.id][value] );
    else
	iframeNode.setAttribute( this.att || this.id, value );
}


/* extract and return video ID from following types of URLs:
   http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
   http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
   http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
   http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
   http://www.youtube.com/embed/0zM3nApSvMg?rel=0
   http://www.youtube.com/watch?v=0zM3nApSvMg
   http://youtu.be/0zM3nApSvMg
 */
function youtube_parser(url) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
    var match = url.match(regExp);
    if (match&&match[2].length==11){
        return match[2];
    }else{
        alert("incorrect url: "+url);
    }
}

// dialog definition
CKEDITOR.dialog.add('youtubeDialog', function (editor) {
    
    var previewPreloader,
    previewAreaHtml = '<div>' + CKEDITOR.tools.htmlEncode(
        editor.lang.common.preview ) + '<br>' +
	'<div id="cke_YoutubePreviewLoader' + CKEDITOR.tools.getNextNumber() + 
        '" style="display:none"><div class="loading">&nbsp;</div></div>' +
	'<div id="cke_YoutubePreviewBox' + CKEDITOR.tools.getNextNumber() + 
        '" class="FlashPreviewBox"></div></div>';
    
    return {
        // basic properties of the dialog window: title, minimum size
        title: 'YouTube Properties',
        minWidth: 350,
        minHeight: 260,
        
        // dialog window contents definition.
        contents:[{
            // definition of the General Info tab (page).
            id: 'info',
            label: 'General',
            accessKey: 'I',
            elements: [{
		type: 'vbox',
		padding: 0,
		children: [{
		    id: 'src',
		    type: 'text',
		    label: editor.lang.common.url,
		    required: true,
		    validate: CKEDITOR.dialog.validate.notEmpty(
                        "URL field cannot be empty"),
		    setup: loadValue,
		    commit: commitValue,
                    onLoad:  function() {
			var dialog = this.getDialog(),
			updatePreview = function(src) {
			    // Query the preloader to figure
                            // out the url impacted by based
                            // href.
                            
                            // update youtube url to an embed url
                            var embedSrc = "http://www.youtube.com/embed/" +
                                youtube_parser(src);
                            previewPreloader.setAttribute('src', embedSrc);
                            
                            dialog.preview.setHtml(
                                '<iframe type="text/html" height="100%" '+
                                    'width="100%" class="youtube-player" src="'+
                                    CKEDITOR.tools.htmlEncode(
                                        previewPreloader.getAttribute(
                                            'src')) +
				    '" frameborder="0" allowfullscreen>'+
                                    '</iframe>' );
			}; // end updatePreview
			// Preview element
			dialog.preview = dialog.getContentElement(
                            'info','preview' ).getElement().getChild( 3 );
                        // Sync on inital value loaded.
			this.on( 'change', function( evt ) {
                            if ( evt.data && evt.data.value )
				updatePreview( evt.data.value);
			});
			// Sync when input value changed.
                        this.getInputElement().on( 'change', function(evt) {
                            updatePreview( this.getValue() );
			}, this);
		    } // end onLoad
		}]
	    },{
		type: 'hbox',
		children: [{
		    type: 'text',
		    id: 'width',
		    style: 'width:100%',
                    'default':'360',
                    labelLayout: 'vertical',
		    label: editor.lang.common.width,
                    validate: CKEDITOR.dialog.validate.notEmpty(
                        "Width field cannot be empty"),
                    //validate: CKEDITOR.dialog.validate.htmlLength(
                    //    editor.lang.common.invalidHtmlLength.replace(
                    //        '%1', editor.lang.common.width ) ),
		    setup: loadValue,
		    commit: commitValue,
                    onLoad:  function() {
                        // when input value changed
                        this.getInputElement().on( 'change', function(evt) {
                            // minimum value is at least 200px
                            if (!(parseInt(this.getValue()) >= 200)) {
                                this.setValue("200");
                            }
                        }, this);
                    }
		},{
		    type: 'text',
		    id: 'height',
		    style: 'width:100%',
                    'default':'200',
                    labelLayout: 'vertical',
		    label: editor.lang.common.height,
                    validate: CKEDITOR.dialog.validate.notEmpty(
                        "Height field cannot be empty"),
                    //validate: CKEDITOR.dialog.validate.htmlLength(
                    //   editor.lang.common.invalidHtmlLength.replace(
                    //     '%1', editor.lang.common.height ) ),
		    setup: loadValue,
		    commit: commitValue,
                    onLoad:  function() {
                        // when input value changed
                        this.getInputElement().on( 'change', function(evt) {
                            // minimum value is at least 200px
                            if (!(parseInt(this.getValue()) >= 200)) {
                                this.setValue("200");
                            }
                        }, this);
                    }
		},{
		    id: 'align',
		    type: 'select',
		    'default': '',
		    items: [
			[ editor.lang.common.notSet, '' ],
			[ editor.lang.common.alignLeft, 'left' ],
			[ editor.lang.common.alignRight, 'right' ],
			[ editor.lang.common.alignTop, 'top' ],
			[ editor.lang.common.alignMiddle, 'middle' ],
			[ editor.lang.common.alignBottom, 'bottom' ]
		    ],
		    style: 'width:100%',
		    labelLayout: 'vertical',
		    label: editor.lang.common.align,
		    setup: function( iframeNode, fakeImage ) {
			loadValue.apply( this, arguments );
			if ( fakeImage ) {
			    var fakeImageAlign =fakeImage.getAttribute('align');
			    this.setValue( fakeImageAlign && 
                                           fakeImageAlign.toLowerCase() || '' );
			}
		    },
		    commit: function(iframeNode, extraStyles, extraAttributes) {
			commitValue.apply( this, arguments );
			if ( this.getValue() )
			    extraAttributes.align = this.getValue();
		    }
		}]
	    },{
		type: 'vbox',
		children: [
		    {
			type: 'html',
			id: 'preview',
			style: 'width:95%;',
			html: previewAreaHtml
		    }
		]
	    }]
        }/*, {
            // definition of the Properties dialog tab (page).
           id: 'properties',
	    label: 'Properties',
	    elements: [{
		type: 'fieldset',
		label: CKEDITOR.tools.htmlEncode('Variables for Youtube'),
		children: [{
		    type: 'vbox',
		    padding: 0,
		    children: [{
			type: 'checkbox',
			id: 'controls',
			label: 'Display player controls',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    },{
			type: 'checkbox',
			id: 'rel',
			label: 'Show related videos',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    },{
			type: 'checkbox',
			id: 'showinfo',
			label: 'Display video info before start'
			'default': true,
			setup: loadValue,
			commit: commitValue
		    },{
			type: 'checkbox',
			id: 'theme',
			label: 'Dark Video player theme',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    }]
		}]
	    }]
        }*/],
            
        
        onShow: function() {
	    // Clear previously saved elements.
	    this.fakeImage = this.iframeNode = null;
            previewPreloader = new CKEDITOR.dom.element(
                'iframe', editor.document );
            
	    var fakeImage = this.getSelectedElement();
	    if ( fakeImage && fakeImage.data( 'cke-real-element-type' ) && 
                 fakeImage.data( 'cke-real-element-type' ) == 'iframe' ) {
		this.fakeImage = fakeImage;
                
		var iframeNode = editor.restoreRealElement( fakeImage );
		this.iframeNode = iframeNode;
                
		this.setupContent( iframeNode );
	    }
	},
        
        
        // method is invoked when a user clicks the OK button, confirming
        // dialog
	onOk: function() {
            // the context of this function is the dialog object itself
            // http://docs.ckeditor.com/#!/api/CKEDITOR.dialog
	    var iframeNode;
	    if ( !this.fakeImage )
		iframeNode = new CKEDITOR.dom.element( 'iframe' );
	    else
		iframeNode = this.iframeNode;
            
	    // A subset of the specified attributes/styles
	    // should also be applied on the fake element to
	    // have better visual effect. (#5240)
	    var extraStyles = {},
	    extraAttributes = {};
	    this.commitContent( iframeNode, extraStyles, extraAttributes );
            
            // update youtube url to an embed url
            var embedSrc = "http://www.youtube.com/embed/" +
                youtube_parser(iframeNode.getAttribute('src'));
            iframeNode.setAttributes({
                'class':'youtube-player',
                'type':'text/html',
                'src':embedSrc,
                'frameborder':'0' 
            });
                                    
	    // Refresh the fake image.
	    var newFakeImage = editor.createFakeElement(
                iframeNode,'cke_youtube', 'iframe', true );
            
	    newFakeImage.setAttributes( extraAttributes );
	    newFakeImage.setStyles( extraStyles );
            
	    if ( this.fakeImage ) {
		newFakeImage.replace( this.fakeImage );
		editor.getSelection().selectElement( newFakeImage );
	    } else
		editor.insertElement( newFakeImage );
                        
	},
        
        onHide: function() {
	    if ( this.preview )
		this.preview.setHtml('');
	}
    };
});
//})();