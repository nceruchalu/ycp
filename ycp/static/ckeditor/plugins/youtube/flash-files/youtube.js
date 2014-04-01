(function() {
// It is possible to set things in three different places.
// 1. As attributes in the object tag.
// 2. As param tags under the object tag.
// 3. As attributes in the embed tag.
// It is possible for a single attribute to be present in more than one place.
// So let's define a mapping between a sementic attribute and its syntactic
// equivalents.
// Then we'll set and retrieve attribute values according to the mapping,
// instead of having to check and set each syntactic attribute every time.
//
// Reference: http://kb.adobe.com/selfservice/viewContent.do?externalId=tn_12701
var ATTRTYPE_OBJECT = 1,
ATTRTYPE_PARAM = 2,
ATTRTYPE_EMBED = 4;

var attributesMap = {
    id: [ {
	type: ATTRTYPE_OBJECT, name: 'id'
    }],
    classid: [ {
	type: ATTRTYPE_OBJECT, name: 'classid'
    }],
    codebase: [ {
	type: ATTRTYPE_OBJECT, name: 'codebase'
    }],
    pluginspage: [ {
	type: ATTRTYPE_EMBED, name: 'pluginspage'
    }],
    src: [ {
	type: ATTRTYPE_PARAM, name: 'movie'
    }, {
	type: ATTRTYPE_EMBED, name: 'src'
    }, {
	type: ATTRTYPE_OBJECT, name: 'data'
    }],
    name: [ {
	type: ATTRTYPE_EMBED, name: 'name'
    }],
    align: [ {
	type: ATTRTYPE_OBJECT, name: 'align'
    }],
    'class': [ {
	type: ATTRTYPE_OBJECT, name: 'class'
    }, {
	type: ATTRTYPE_EMBED, name: 'class'
    }],
    width: [ {
	type: ATTRTYPE_OBJECT, name: 'width'
    }, {
	type: ATTRTYPE_EMBED, name: 'width'
    }],
    height: [ {
	type: ATTRTYPE_OBJECT, name: 'height'
    }, {
	type: ATTRTYPE_EMBED, name: 'height'
    }],
    hSpace: [ {
	type: ATTRTYPE_OBJECT, name: 'hSpace'
    }, {
	type: ATTRTYPE_EMBED, name: 'hSpace'
    }],
    vSpace: [ {
	type: ATTRTYPE_OBJECT, name: 'vSpace'
    }, {
	type: ATTRTYPE_EMBED, name: 'vSpace'
    }],
    style: [ {
	type: ATTRTYPE_OBJECT, name: 'style'
    }, {
	type: ATTRTYPE_EMBED, name: 'style'
    }],
    type: [ {
	type: ATTRTYPE_EMBED, name: 'type'
    }]
};

var names = [ 'play', 'loop', 'menu', 'quality', 'scale', 'salign', 'wmode', 
              'bgcolor', 'base', 'flashvars', 'allowScriptAccess', 
              'allowFullScreen' ];
for ( var i = 0; i < names.length; i++ )
    attributesMap[ names[ i ] ] = [ {
	type: ATTRTYPE_EMBED, name: names[ i ]
    }, {
	type: ATTRTYPE_PARAM, name: names[ i ]
    }];
names = [ 'allowFullScreen', 'play', 'loop', 'menu' ];
for ( i = 0; i < names.length; i++ )
    attributesMap[ names[ i ] ][ 0 ][ 'default' ] = 
        attributesMap[ names[ i ] ][ 1 ][ 'default' ] = true;

var defaultToPixel = CKEDITOR.tools.cssLength;

function loadValue( objectNode, embedNode, paramMap ) {
    var attributes = attributesMap[ this.id ];
    if ( !attributes )
	return;
    
    var isCheckbox = ( this instanceof CKEDITOR.ui.dialog.checkbox );
    for ( var i = 0; i < attributes.length; i++ ) {
	var attrDef = attributes[ i ];
	switch ( attrDef.type ) {
	case ATTRTYPE_OBJECT:
	    if ( !objectNode )
		continue;
	    if ( objectNode.getAttribute( attrDef.name ) !== null ) {
		var value = objectNode.getAttribute( attrDef.name );
		if ( isCheckbox )
		    this.setValue( value.toLowerCase() == 'true' );
		else
		    this.setValue( value );
		return;
	    } else if ( isCheckbox )
		this.setValue( !!attrDef[ 'default' ] );
	    break;
	case ATTRTYPE_PARAM:
	    if ( !objectNode )
		continue;
	    if ( attrDef.name in paramMap ) {
		value = paramMap[ attrDef.name ];
		if ( isCheckbox )
		    this.setValue( value.toLowerCase() == 'true' );
		else
		    this.setValue( value );
		return;
	    } else if ( isCheckbox )
		this.setValue( !!attrDef[ 'default' ] );
	    break;
	case ATTRTYPE_EMBED:
	    if ( !embedNode )
		continue;
	    if ( embedNode.getAttribute( attrDef.name ) ) {
		value = embedNode.getAttribute( attrDef.name );
		if ( isCheckbox )
		    this.setValue( value.toLowerCase() == 'true' );
		else
		    this.setValue( value );
		return;
	    } else if ( isCheckbox )
		this.setValue( !!attrDef[ 'default' ] );
	}
    }
}

function commitValue( objectNode, embedNode, paramMap ) {
    var attributes = attributesMap[ this.id ];
    if ( !attributes )
	return;
    
    var isRemove = ( this.getValue() === '' ),
    isCheckbox = ( this instanceof CKEDITOR.ui.dialog.checkbox );
    
    for ( var i = 0; i < attributes.length; i++ ) {
	var attrDef = attributes[ i ];
	switch ( attrDef.type ) {
	case ATTRTYPE_OBJECT:
	    // Avoid applying the data attribute when not needed (#7733)
	    if ( !objectNode || ( attrDef.name == 'data' && embedNode && 
                                  !objectNode.hasAttribute( 'data' ) ) )
		continue;
	    var value = this.getValue();
	    if ( isRemove || isCheckbox && value === attrDef[ 'default' ] )
		objectNode.removeAttribute( attrDef.name );
	    else
		objectNode.setAttribute( attrDef.name, value );
	    break;
	case ATTRTYPE_PARAM:
	    if ( !objectNode )
		continue;
	    value = this.getValue();
	    if ( isRemove || isCheckbox && value === attrDef[ 'default' ] ) {
		if ( attrDef.name in paramMap )
		    paramMap[ attrDef.name ].remove();
	    } else {
		if ( attrDef.name in paramMap )
		    paramMap[ attrDef.name ].setAttribute( 'value', value );
		else {
		    var param = CKEDITOR.dom.element.createFromHtml(
                        '<cke:param></cke:param>', objectNode.getDocument() );
		    param.setAttributes({ name: attrDef.name, value: value } );
		    if ( objectNode.getChildCount() < 1 )
			param.appendTo( objectNode );
		    else
			param.insertBefore( objectNode.getFirst() );
		}
	    }
	    break;
	case ATTRTYPE_EMBED:
	    if ( !embedNode )
		continue;
	    value = this.getValue();
	    if ( isRemove || isCheckbox && value === attrDef[ 'default' ] )
		embedNode.removeAttribute( attrDef.name );
	    else
		embedNode.setAttribute( attrDef.name, value );
	}
    }
}

// dialog definition
CKEDITOR.dialog.add('youtubeDialog', function (editor) {
    var makeObjectTag = true,
    makeEmbedTag = true;
    
    var previewPreloader,
    previewAreaHtml = '<div>' + CKEDITOR.tools.htmlEncode(
        editor.lang.common.preview ) + '<br>' +
	'<div id="cke_FlashPreviewLoader' + CKEDITOR.tools.getNextNumber() + 
        '" style="display:none"><div class="loading">&nbsp;</div></div>' +
	'<div id="cke_FlashPreviewBox' + CKEDITOR.tools.getNextNumber() + 
        '" class="FlashPreviewBox"></div></div>';

    return {
        // basic properties of the dialog window: title, minimum size
        title: 'YouTube Properties',
        minWidth: 420,
        minHeight: 310,
        
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
		    type: 'hbox',
		    widths: ['280px', '110px'],
		    align: 'right',
		    children: [{
			id: 'src',
			type: 'text',
			label: 'URL',
			required: true,
			validate: CKEDITOR.dialog.validate.notEmpty(
                            "URL field cannot be empty"),
			setup: loadValue,
			commit: commitValue,
			onLoad: function() {
			    var dialog = this.getDialog(),
			    updatePreview = function( src ) {
				// Query the preloader to figure
                                // out the url impacted by based
                                // href.
				previewPreloader.setAttribute('src', src);
				dialog.preview.setHtml(
                                    '<embed height="100%" width="100%" src="' +
                                        CKEDITOR.tools.htmlEncode(
                                            previewPreloader.getAttribute(
                                                'src'))
					+ '" type="application/x-shockwave-flash"></embed>' );
			    };
			    // Preview element
			    dialog.preview = dialog.getContentElement(
                                'info','preview' ).getElement().getChild( 3 );
                            
			    // Sync on inital value loaded.
			    this.on( 'change', function( evt ) {
                                
				if ( evt.data && evt.data.value )
				    updatePreview( evt.data.value );
			    });
			    // Sync when input value changed.
			    this.getInputElement().on( 'change', function(evt) {
                                updatePreview( this.getValue() );
			    }, this );
			}
		    }]
		}]
	    },{
		type: 'hbox',
		widths: [ '25%', '25%', '25%', '25%', '25%' ],
		children: [{
		    type: 'text',
		    id: 'width',
		    style: 'width:95px',
		    label: editor.lang.common.width,
		    validate: CKEDITOR.dialog.validate.htmlLength(
                        editor.lang.common.invalidHtmlLength.replace(
                            '%1', editor.lang.common.width ) ),
		    setup: loadValue,
		    commit: commitValue
		},{
		    type: 'text',
		    id: 'height',
		    style: 'width:95px',
		    label: editor.lang.common.height,
		    validate: CKEDITOR.dialog.validate.htmlLength(
                        editor.lang.common.invalidHtmlLength.replace(
                            '%1', editor.lang.common.height ) ),
		    setup: loadValue,
		    commit: commitValue
		},{
		    type: 'text',
		    id: 'hSpace',
		    style: 'width:95px',
		    label: 'HSpace',
		    validate: CKEDITOR.dialog.validate.integer(
                        "HSpace must be a number" ),
		    setup: loadValue,
		    commit: commitValue
		},{
		    type: 'text',
		    id: 'vSpace',
		    style: 'width:95px',
		    label: 'VSpace',
		    validate: CKEDITOR.dialog.validate.integer(
                        "VSpace must be a number" ),
		    setup: loadValue,
		    commit: commitValue
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
        },{
            // definition of the Properties dialog tab (page).
           id: 'properties',
	    label: 'Properties',
	    elements: [{
		type: 'hbox',
		widths: [ '50%', '50%' ],
		children: [{
		    id: 'scale',
		    type: 'select',
		    label: 'Scale',
		    'default': '',
		    style: 'width : 100%;',
		    items: [
			[ editor.lang.common.notSet, '' ],
			[ 'Show all', 'showall' ],
			[ 'No border', 'noborder' ],
			[ 'Exact fit', 'exactfit' ]
		    ],
		    setup: loadValue,
		    commit: commitValue
		},{
		    id: 'allowScriptAccess',
		    type: 'select',
		    label: 'Script Access',
		    'default': '',
		    style: 'width : 100%;',
		    items: [
			[ editor.lang.common.notSet, '' ],
			[ 'Always', 'always' ],
			[ 'Same domain', 'samedomain' ],
			[ 'Never', 'never' ]
		    ],
		    setup: loadValue,
		    commit: commitValue
		}]
	    },{
		type: 'hbox',
		widths: [ '50%', '50%' ],
		children: [{
		    id: 'wmode',
		    type: 'select',
		    label: 'Window mode',
		    'default': '',
		    style: 'width : 100%;',
		    items: [
			[ editor.lang.common.notSet, '' ],
			[ 'Window', 'window' ],
			[ 'Opaque', 'opaque' ],
			[ 'Transparent','transparent']
		    ],
		    setup: loadValue,
		    commit: commitValue
		},{
		    id: 'quality',
		    type: 'select',
		    label: 'Quality',
		    'default': 'high',
		    style: 'width : 100%;',
		    items: [
			[ editor.lang.common.notSet, '' ],
			[ 'Best', 'best' ],
			[ 'High', 'high' ],
			[ 'Auto High', 'autohigh' ],
			[ 'Medium', 'medium' ],
			[ 'Auto Low', 'autolow' ],
			[ 'Low', 'low' ]
		    ],
		    setup: loadValue,
		    commit: commitValue
		}]
	    },{
		type: 'hbox',
		widths: [ '50%', '50%' ],
		children: [{
		    id: 'align',
		    type: 'select',
		    label: editor.lang.common.align,
		    'default': '',
		    style: 'width : 100%;',
		    items: [
			[ editor.lang.common.notSet, '' ],
			[ editor.lang.common.alignLeft, 'left' ],
			[ 'Abs Bottom', 'absBottom' ],
			[ 'Abs Middle', 'absMiddle' ],
			[ 'Baseline', 'baseline' ],
			[ editor.lang.common.alignBottom, 'bottom' ],
			[ editor.lang.common.alignMiddle, 'middle' ],
			[ editor.lang.common.alignRight, 'right' ],
			[ 'Text Top', 'textTop' ],
			[ editor.lang.common.alignTop, 'top' ]
		    ],
		    setup: loadValue,
		    commit: function( objectNode, embedNode, paramMap,
                                      extraStyles, extraAttributes ) {
			var value = this.getValue();
			commitValue.apply( this, arguments );
			value && ( extraAttributes.align = value );
		    }
		},{
		    type: 'html',
		    html: '<div></div>'
		}]
	    },{
		type: 'fieldset',
		label: CKEDITOR.tools.htmlEncode('Variables for Youtube'),
		children: [{
		    type: 'vbox',
		    padding: 0,
		    children: [{
			type: 'checkbox',
			id: 'menu',
			label: 'Enable Flash Menu',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    },{
			type: 'checkbox',
			id: 'play',
			label: 'Auto Play',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    },{
			type: 'checkbox',
			id: 'loop',
			label: 'Loop',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    },{
			type: 'checkbox',
			id: 'allowFullScreen',
			label: 'Allow Fullscreen',
			'default': true,
			setup: loadValue,
			commit: commitValue
		    }]
		}]
	    }]
        }],
        
        
        onShow: function() {
	    // Clear previously saved elements.
	    this.fakeImage = this.objectNode = this.embedNode = null;
	    previewPreloader = new CKEDITOR.dom.element(
                'embed', editor.document );
            
	    // Try to detect any embed or object tag that has Flash parameters.
	    var fakeImage = this.getSelectedElement();
	    if ( fakeImage && fakeImage.data( 'cke-real-element-type' ) && 
                 fakeImage.data( 'cke-real-element-type' ) == 'flash' ) {
		this.fakeImage = fakeImage;
                
		var realElement = editor.restoreRealElement( fakeImage ),
		objectNode = null,
		embedNode = null,
		paramMap = {};
		if ( realElement.getName() == 'cke:object' ) {
		    objectNode = realElement;
		    var embedList = objectNode.getElementsByTag( 'embed','cke');
		    if ( embedList.count() > 0 )
			embedNode = embedList.getItem( 0 );
		    var paramList = objectNode.getElementsByTag( 'param','cke');
		    for ( var i=0, length=paramList.count(); i < length; i++ ) {
			var item = paramList.getItem( i ),
			name = item.getAttribute( 'name' ),
			value = item.getAttribute( 'value' );
			paramMap[ name ] = value;
		    }
		} else if ( realElement.getName() == 'cke:embed' )
		    embedNode = realElement;
                
		this.objectNode = objectNode;
		this.embedNode = embedNode;
                
		this.setupContent( objectNode, embedNode, paramMap, fakeImage );
	    }
	},
        
        
        // method is invoked when a user clicks the OK button, confirming dialog
        /*onOk: function() {
            // the context of this function is the dialog object itself
            // http://docs.ckeditor.com/#!/api/CKEDITOR.dialog
            var dialog = this;
            var html = '<div class="youtube-player-wrapper"><object width="640" height="360"><param name="movie" value="https://www.youtube.com/v/pNemhViwJpU?version=3"><param name="allowFullScreen" value="true"><param name="allowScriptAccess" value="always"><embed src="https://www.youtube.com/v/pNemhViwJpU?version=3" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="640" height="360"></object></div>'
            // insert the element at the editor caret position
            editor.insertHtml(html);
            }*/
        onOk: function() {
	    // If there's no selected object or embed, create one. Otherwise, 
	    // reuse the selected object and embed nodes.
	    var objectNode = null,
	    embedNode = null,
	    paramMap = null;
	    if ( !this.fakeImage ) {
		if ( makeObjectTag ) {
		    objectNode = CKEDITOR.dom.element.createFromHtml(
                        '<cke:object></cke:object>', editor.document );
		    var attributes = {
			classid: 'clsid:d27cdb6e-ae6d-11cf-96b8-444553540000',
			codebase: 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0'
		    };
		    objectNode.setAttributes( attributes );
		}
		if ( makeEmbedTag ) {
		    embedNode = CKEDITOR.dom.element.createFromHtml(
                        '<cke:embed></cke:embed>', editor.document );
		    embedNode.setAttributes({
			type: 'application/x-shockwave-flash',
			pluginspage: 'http://www.macromedia.com/go/getflashplayer'
		    });
		    if ( objectNode )
			embedNode.appendTo( objectNode );
		}
	    } else {
		objectNode = this.objectNode;
		embedNode = this.embedNode;
	    }
            
	    // Produce the paramMap if there's an object tag.
	    if ( objectNode ) {
		paramMap = {};
		var paramList = objectNode.getElementsByTag( 'param', 'cke' );
		for ( var i = 0, length = paramList.count(); i < length; i++ ) {
		    paramMap[ paramList.getItem( i ).getAttribute( 'name' ) ] = 
                        paramList.getItem( i );
                }
	    }
            
	    // A subset of the specified attributes/styles
	    // should also be applied on the fake element to
	    // have better visual effect. (#5240)
	    var extraStyles = {},
	    extraAttributes = {};
	    this.commitContent( objectNode, embedNode, paramMap, extraStyles, 
                                extraAttributes );
            
	    // Refresh the fake image.
	    var newFakeImage = editor.createFakeElement(objectNode || embedNode,
                                                        'cke_youtube', 'flash', 
                                                        true );
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



})();