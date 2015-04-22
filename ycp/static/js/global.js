$(document).ready(function(){ // container for entire script

    // base domain should be "http://consortiumforprogress.com" but the domain
    // has been lost :(
    var BASE_DOMAIN = "http://ycp.nnoduka.com";
    
    if($(".homepage").length > 0) { // ensure you are on homepage
        var icons = [
            "#about-",
            "#projects-",
            "#posts-",
            "#photos-",
            "#getinvolved-",
        ];
        
        /* calculate x and y coordinates for icons on homepage */
        var startAngle = Math.PI*0.05, 
        angleSpacing = (Math.PI-startAngle)/(icons.length - 1),
        angle = Math.PI - startAngle/2,
        radius = 230, /* in px */
        offset = ($("#page-icons").width() - $("#page-icons a").width())/2,
        left = 0,
        bottom = 0,
        rotate = "";
        
        for(var i=0; i<icons.length; i++) {
            left = radius * Math.cos(angle) + offset;
            bottom  = radius * Math.sin(angle);
            rotate =  "rotate(" + (180- angle*180/Math.PI) + "deg)"
            $(icons[i]+"icon")
                .css("left", left + "px")
                .css("bottom", bottom + "px");
            
            $(icons[i]+"line")
                .css("width", (radius - 125 - 5) + "px") // 5px "margin"
                .css("left", (left+$("#page-icons a").width()/2) + "px")
                .css("bottom", bottom + "px")
                .css("transform", rotate)
                .css("-ms-transform", rotate)
                .css("-webkit-transform", rotate)
                .css("-moz-transform", rotate)
                .css("-o-transform", rotate);
                        
            angle -= angleSpacing;
        }
        
        $('#slider').nivoSlider(); /* load slider */
        
        // fix up "what's new" section -- replace videos and pictures
        $("#recent-posts .blog-snippet iframe")
            .replaceWith('<span>[YouTube Video]</span>');
        $("#recent-posts .blog-snippet img")
            .replaceWith('<span>[Image]</span>');
    } // end homepage functions
    
    
    
    // delete form confirmation Box
    function confirmationBox(event) {
        var form = $(event.currentTarget);
        var options = { 
            animation: 200,
            override: false,
	    buttons: { 
                cancel: {
                    text: 'No',
                    className: 'blue',
                    action: function() {  // Callback function
		        Apprise('close');
                    }   
                },
                confirm: {
                    text: 'Yes',          // Button text
                    className: 'red',     // Custom class name(s)
                    action: function() {  // Callback function
		        form.unbind("submit");
                        Apprise('close'); 
                        form.submit();
                    }                     // end Callback function
		}                         // end confirm
	    },
	};
        
        var apprise_text = "Are you sure you want to "+ 
            (form.attr("title") || "delete") + "?";
	Apprise(apprise_text, options);
        return false;
    };
    $('form.delete').submit(confirmationBox);
    
    
    
    // share on social media
    function winPop (location) {
        window.open (location, "_blank",
                     "status=1,toolbar=0, location=0, menubar=0,directories=0,resizeable=0, width=700, height=350");
        }
    
    function bindShareEvents() {
        // hide share media inputs and buttons
        $(".share-media").hide();
        
        // on share button click, toggle share media buttons and select input
        $(".share-icon.button").unbind('click').click(function () {
            $(".share-media").toggle(300);
            $(".share-media input").select();
        });
        
        // share on facebook
        $(".share-media a.facebook")
            .unbind('click')
            .click(function() {
                var location = "https://www.facebook.com/sharer.php?u="+
                    encodeURIComponent($(this).parent(".share-media")
                                       .data("url"))+"&t"+
                    encodeURIComponent($(this).parent(".share-media")
                                       .data("title"));
                winPop(location);
            });
        
        // share on twitter
        $(".share-media a.twitter")
            .unbind('click')
            .click(function() {
                var location = "http://twitter.com/share?text="+
                    encodeURIComponent("#ycp "+ $(this).parent(".share-media")
                                       .data("title")) +
                    "&url="+ encodeURIComponent($(this).parent(".share-media")
                                                .data("url"));
                winPop(location);
            });
    }
    bindShareEvents();
    // end share media
    
    
    
     
    function removeWaitAnimation() {
        // Remove the wait animation and message
        $('.ajax-loader').remove();
    }
    
    /*
     * this functionality should only exist on a gallery page where thumbnails
     * are clicked and expand to detail views
     */
    if($("#gallery.expandable-thumbnails").length > 0) {
        
        function createGalleryDetail(thumbnail, callback) {
            
            
            thumbnail.prepend('<div class="ajax-loader"> </div>');
            
            // get div details via ajax
            $.ajax({
                type:'GET',
                url:thumbnail.data("url").replace(/\s+/g, ""),
                success: function(data) {
                    removeWaitAnimation();
                    callback(data, thumbnail);
                },
                error: function(data) {
                    removeWaitAnimation();
                },
                dataType: 'json'
            });
        }
        
        /* see: https://developers.google.com/youtube/youtube_player_demo */
        function createGalleryDetailCallback(data, thumbnail) {
            var url = data['url'],
            title = data['title'],
            user = data['user'],
            description = data['description'],
            type = thumbnail.data("type"),
            mediaid = thumbnail.data("mediaid"),
            mid = thumbnail.data("mid"), // photo or video id
            created = thumbnail.data("created"),
            comments_count = thumbnail.data("commentscount"),
            tags = data['tags'],
            comments = data['comments_html'],
            media = '';
            var share_button = '<a href="javascript:;" ' +
                'class="share-icon button" title="share">Share' +
                '<span class="icon"></span></a>';
            var edit_button =
                '<a href="/'+type+'/edit/'+mid+'/" class="edit-icon icon"' +
                ' title="edit media"></a>';
            var delete_button = 
                '<form action="/'+type+'/delete/'+mid+'/" method="post" ' +
                ' class="delete" title="delete media">' +
                csrf_token +
                '<button type="submit" class="delete-icon icon"></button>'+
                '</form>';
            
            var share_media = 
                '<div class="share-media"'+
                '    data-url="'+BASE_DOMAIN + '/media/' + mediaid + '/" '+
                '    data-title="'+title+'">'+
                '    <a href="javascript:;" class="share-icon icon facebook">'+
                '    </a>'+
                '    <a href="javascript:;" class="share-icon icon twitter">'+
                '    </a>'+
                '    <input type="text"'+
                '     value="'+BASE_DOMAIN+ '/media/'+ mediaid + '/" />' +
                '<div class="clear"></div>'+
                '</div>';
                                    
            if (type=="photo") {
                media = '<img src="' + url + '" alt="detailed image"/>';
                if (!can_edit_photo) {
                    edit_button = '';
                }
                if (!can_delete_photo) {
                    delete_button = '';
                }
            } else {
                media =
                    '<div class="youtube-player-wrapper">'+
                    '<iframe class="youtube-player" type="text/html" '+
                    'width="640" height="360" '+
                    'src="http://www.youtube.com/embed/'+url+'" '+
                    'frameborder="0" allowfullscreen></iframe></div>';
                /*
                media =
                    '<div class="youtube-player-wrapper">'+
                    '<object width="640" height="360">'+
                    '<param name="movie" value="https://www.youtube.com/v/'+
                    url+'?version=3"></param>'+
                    '<param name="allowFullScreen" value="true"></param>'+
                    '<param name="allowScriptAccess" value="always"></param>'+
                    '<embed src="https://www.youtube.com/v/'+url+
                    '?version=3" type="application/x-shockwave-flash" '+
                    'allowfullscreen="true" allowScriptAccess="always" '+
                    'width="640" height="360"></embed></object></div>';
                */
                if (!can_edit_video) {
                    edit_button = '';
                }
                if (!can_delete_video) {
                    delete_button = '';
                }
            }
            
                   
            if(url) {
                // tags_html
                var tags_html = '';
                for (var i = 0; i < tags.length; i++) {
                    tags_html += '<a href="/tag/'+encodeURIComponent(tags[i])+
                                  '">' +  tags[i] + '</a>';
                    if (i < tags.length-1) tags_html += ', ';
                }
                // metadata
                var meta_html =
                    '<div class="meta">' +
                    '  <span class="created"><span class="icon"></span>' +
                    '    Posted ' + created + ' by '+user+'</span>' +
                    '  <span class="comments-count"><span class="icon"></span> '+
                         comments_count + 
                    '    comment' + ((parseInt(comments_count) != 1) ?'s' :'') +
                    '  </span>' +
                    '  <span class="tags"><span class="icon"></span>Tags: ' + 
                         tags_html +'</span>' +
                    '</div>';
                
                // create detail div
                var detail_html = 
                    '<div class="detail">' +
                    '  <div class="arrow"></div>' +
                    '  <h2>'+title+'</h2>' +
                       meta_html +
                    '  <span class="close icon" title="close '+title +
                    '"></span>' +
                       media +
                    '  <p class="description">'+description+'</p>' +
                    '  <div class="icon-container"> '+
                         delete_button +edit_button +share_button +share_media +
                    '  </div>' +
                    '</div>' +
                    '<div class="clear"></div>'+
                    '<div id="comments" class="comments-container">' +
                    '  <h2>Comments</h2>' +
                    '  <div class="comment-form">'+
                    '    <a href="/media/'+mediaid+'/#comments" '+
                    '       target="_blank" class="add-icon">' +
                    '       <button type="button">Add/ View All'+
                    '          </button></a>'+
                    '  </div>' +
                       comments +
                    '</div>';
                var detail = $('<div class="detailwrap">'+detail_html+'</div>');
                // attach delete button confirmation box handler
                detail.find("form.delete").submit(confirmationBox);

                thumbnail.hide();                        // hide thumbnail
                $(".thumbnail img").addClass("hover");   // and hover others

                thumbnail.after(detail);                 // insert detail
                bindShareEvents();
                
                // when you click close, hide this and show thumbnail
                detail.find(".close").click(function() {
                    if(type =="photo") {
                        // for a photo, just hide detail
                        $(this).closest(".detailwrap").hide();
                    } else {
                        // for a video, remove detail, so it won't keep playing
                        // in background
                        $(this).closest(".detailwrap").remove();
                    }
                    thumbnail.show();
                    $(".thumbnail img").removeClass("hover");
                });
            } // end if(url)
        }
        
        
        $(".thumbnail").click(function() { // when a thumbnail is clicked
            $(".detailwrap .close").click();   // first close any open detail
            
                        
            // only create detail div it doesnt already exist
            if ($(this).siblings(".detailwrap").length == 0) {
                // create detail
                createGalleryDetail($(this), createGalleryDetailCallback);
                
            // if detail div already exists, just show it
            } else {
                $(this).hide();                        // hide thumbnail
                $(".thumbnail img").addClass("hover"); // and hover others
                $(this).siblings(".detailwrap").show();
            }
            
        });                       
    }
    
    
    // LOAD OLDER COMMENTS
    function ajaxCommentsLoad() {
        // temporarirly disable button -- dont want clicks during ajax get
        $("#more-comments").prop('disabled', true)
        var url = $("#more-comments").data("url");
        
        // load old comments via AJAX
        $.ajax({
            url:url,
            success: function(data) {
                commentsLoadSuccess(data);
            },
            error:function(data) {
                // nothing here
            },
            dataType:'json'
        });
        return false;
    }
    
    function commentsLoadSuccess(data) {
        if (data['next_page'] == 0) { // cant load any more
            $("#more-comments").hide();
        } else {
            var url_patt = /(page=[\S]+)/i;
            var url =  $("#more-comments").data("url");
            url = url.replace(url_patt,"page="+data['next_page']);
            $("#more-comments").data("url", url);
        }
        $("#comments ul").append(data['comments_html']);
        $("#more-comments").prop('disabled',false); // renable button
    }
    
    $("#more-comments").click(function(event) {
        ajaxCommentsLoad();
    });

}); // end container for entire script