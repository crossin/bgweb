/*
 *         developed by Matteo Bicocchi on JQuery
 *         © 2002-2009 Open Lab srl, Matteo Bicocchi
 *			    www.open-lab.com - info@open-lab.com
 *       	version 1.5.5
 *       	tested on: 	Explorer and FireFox for PC
 *                  		FireFox and Safari for Mac Os X
 *                  		FireFox for Linux
 *         MIT - GPL (GPL-LICENSE.txt) licenses.
 *
 * CONTAINERS BUILD WITH BLOCK ELEMENTS
 */

(function($){
	var msie6=$.browser.msie && $.browser.version=="6.0";
	var Opera=$.browser.opera;
	var zi=100;
	jQuery.fn.buildContainers = function (options){
		return this.each (function ()
		{
			if ($(this).is("[inited=true]")) return;

			this.options = {
				containment:"document",
				elementsPath:"elements/",
				onMinimize:function(){},
				onIconize:function(){},
				onClose: function(){},
				minimizeEffect:"slide", //or "fade"
				effectDuration:300
			}

			$.extend (this.options, options);
			var container=$(this);
			container.attr("inited","true");
			$(this).attr("options",this.options)
			if ($.metadata){
				$.metadata.setType("class");
				if (container.metadata().skin) container.attr("skin",container.metadata().skin);
				if (container.metadata().minimized) container.attr("minimized",container.metadata().minimized);
				if (container.metadata().iconized) container.attr("iconized",container.metadata().iconized);
				if (container.metadata().icon) container.attr("icon",container.metadata().icon);
				if (container.metadata().buttons) container.attr("buttons",container.metadata().buttons);

				if (container.metadata().width) container.attr("width",container.metadata().width);
				if (container.metadata().height) container.attr("height",container.metadata().height);
			}

			container.addClass(container.attr("skin"));
			if (!container.attr("minimized")) container.attr("minimized","false");
			container.find(".n:first").attr("unselectable","on");
			if (!container.find(".n:first").html()) container.find(".n:first").html("&nbsp;")
			container.setIcon(container.attr("icon"), this.options.elementsPath);
			container.setButtons(container.attr("buttons"),this.options);
			if (container.attr("width")){
				var cw= $.browser.msie? container.attr("width"):container.attr("width")+"px";
				container.css({width:cw});
			}

			if (container.attr("height")){
				container.find(".c:first , .content:first").css("height",container.attr("height")-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight()));
			}

			if (container.hasClass("draggable")){
				container.css({position:"absolute", margin:0});
				container.find(".n:first").css({cursor:"move"});
				container.css({zIndex:zi++});
				container.draggable({handle:".n:first",cancel:".c",delay:0, containment:this.options.containment});
				container.bind("mousedown",function(){
					$(this).mb_BringToFront();
				});
			}
			if (container.hasClass("resizable")){
				container.containerResize();
			}
			if (container.attr("minimized")=="true"){
				container.attr("minimized","false");
				container.minimize(this.options);
			}
			if (container.attr("iconized")=="true"){
				container.attr("iconized","false");
				container.iconize(this.options);
			}
		});
	}

	jQuery.fn.containerResize = function (){
		var isDraggable=$(this).hasClass("draggable");
		$(this).resizable({
			handles:isDraggable ? "":"s",
			minWidth: 150,
			minHeight: 150,
			iframeFix:true,
			//autoHide: !$.browser.msie,
			helper: "mbproxy",
			start:function(e,o){
				o.helper.mb_BringToFront();
			},
			stop:function(e,o){
				var resCont= $(this);//$.browser.msie || Opera ?o.helper:
				var elHeight= resCont.outerHeight()-$(this).find(".n:first").outerHeight()-($(this).find(".s:first").outerHeight());
				$(this).find(".c:first , .content:first").css({height: elHeight});
				if (!isDraggable){
					var elWidth=$(this).attr("width") && $(this).attr("width")>0 ?$(this).attr("width"):"100%";
					$(this).css({width: elWidth});
				}
			}
		});
		$(this).find(".ui-resizable-s").addClass("mb-resize");
		$(this).find(".ui-resizable-se").addClass("mb-resize");
		$(this).find(".ui-resizable-w").addClass("mb-resize");
		$(this).find(".ui-resizable-e").addClass("mb-resize");
	}

	jQuery.fn.setIcon = function (icon,path){
		if (icon && icon!="" ){
			$(this).find(".ne:first").prepend("<img class='icon' src='"+path+"icons/"+icon+"' style='position:absolute'>");
			$(this).find(".n:first").css({paddingLeft:15});
		}else{
			$(this).find(".n:first").css({paddingLeft:0});
		}
	}

	jQuery.fn.setButtons = function (buttons,opt){
		var path= opt.elementsPath;
		var container=$(this);
		if (buttons !=""){
			var btn=buttons.split(",");
			$(this).find(".ne:first").append("<div class='buttonBar'></div>");
			for (var i in btn){
				if (btn[i]=="c"){
					$(this).find(".buttonBar:first").append("<img src='"+path+$(this).attr('skin')+"/close.png' class='close'>");
					$(this).find(".close:first").bind("click",function(){
						container.fadeOut(200);
						opt.onClose();
					});
				}
				if (btn[i]=="m"){
					$(this).find(".buttonBar:first").append("<img src='"+path+$(this).attr('skin')+"/min.png' class='minimizeContainer'>");
					$(this).find(".minimizeContainer:first").bind("click",function(){container.minimize(opt)});
					$(this).find(".n:first").bind("dblclick",function(){container.minimize(opt)});
				}
				if (btn[i]=="p"){
					$(this).find(".buttonBar:first").append("<img src='"+path+$(this).attr('skin')+"/print.png' class='printContainer'>");
					$(this).find(".printContainer:first").bind("click",function(){});
				}
				if (btn[i]=="i"){
					$(this).find(".buttonBar:first").append("<img src='"+path+$(this).attr('skin')+"/iconize.png' class='iconizeContainer'>");
					$(this).find(".iconizeContainer:first").bind("click",function(){container.iconize(opt)});
				}
			}
			var fadeOnClose=$.browser.mozilla || $.browser.safari;
			if (fadeOnClose) $(this).find(".buttonBar:first img").css({opacity:.5, cursor:"pointer","mozUserSelect": "none", "khtmlUserSelect": "none"}).mouseover(function(){$(this).fadeTo(200,1)}).mouseout(function(){if (fadeOnClose)$(this).fadeTo(200,.5)});
			$(this).find(".buttonBar:first img").attr("unselectable","on");
		}
	}

	jQuery.fn.minimize = function (opt){
		this.each (function ()
		{
			var container=$(this);
			if ($(this).attr("minimized")=="false"){
				this.w = container.outerWidth();
				this.h = container.outerHeight();
				if (opt.minimizeEffect=="fade")
					container.find(".o:first").fadeOut(opt.effectDuration,function(){});
				else{
					container.find(".icon:first").hide();
					container.find(".o:first").slideUp(opt.effectDuration,function(){});
					container.animate({height:container.find(".n:first").outerHeight()+container.find(".s:first").outerHeight()},opt.effectDuration,function(){container.find(".icon:first").show()});
				}
				container.attr("minimized","true");
				container.find(".minimizeContainer:first").attr("src",opt.elementsPath+$(this).attr('skin')+"/max.png");
				container.resizable("destroy");
				if (opt.onMinimize) opt.onMinimize();
			}else{
				if (opt.minimizeEffect=="fade")
					container.find(".o:first").fadeIn(opt.effectDuration,function(){});
				else{
					container.find(".o:first").slideDown(opt.effectDuration,function(){});
					container.find(".icon:first").hide();
					container.animate({height:this.h},opt.effectDuration,function(){container.find(".icon:first").show()});
				}
				if (container.hasClass("resizable")) container.containerResize();
				container.attr("minimized","false");
				container.find(".minimizeContainer:first").attr("src",opt.elementsPath+$(this).attr('skin')+"/min.png");

			}
		})
	}

	jQuery.fn.iconize = function (opt){
		if (!opt) opt=$(this).attr("options");
		return this.each (function ()
		{
			var container=$(this);
			this.h = container.outerHeight();
			container.attr("iconized","true");
			if(container.attr("minimized")=="false"){
				container.attr("w",container.attr("width") && container.attr("width")>0 ? (!container.hasClass("resizable")? container.attr("width"):container.width()):"100%");
				container.attr("h",container.height());
			}
			container.attr("t",container.css("top"));
			container.attr("l",container.css("left"));
			container.resizable("destroy");
			if (!$.browser.msie) {
				container.find(".no:first").slideUp("fast");
				container.animate({ height:"32px", width:"32px",left:0},opt.effectDuration);
			}else{
				container.find(".no:first").hide();
				container.css({ height:"32px", width:"32px",left:0});
			}
			container.append("<img src='"+opt.elementsPath+"/icons/"+(container.attr("icon")?container.attr("icon"):"restore.png")+"' class='restoreContainer' width='32'>");
			if (opt.onIconize) opt.onIconize();
			container.find(".restoreContainer:first").bind("click",function(){
				container.attr("iconized","false");
				if (!$.browser.msie) {
					container.find(".no:first").fadeIn("fast");
					if(container.attr("minimized")=="false")
						container.animate({height:container.attr("h"), width:container.attr("w"),left:container.attr("l")},opt.effectDuration);
					else
						container.animate({height:"60px", width:container.attr("w"),left:container.attr("l")},opt.effectDuration);

					container.find(".c:first , .content:first").css("height",container.attr("h")-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight()));
				} else {
					container.find(".no:first").show();
					container.css({ width:container.attr("w"),left:container.attr("l"), height:container.attr("h")});
					container.find(".c:first , .content:first").css("height",container.attr("h")-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight()));
					container.css({})
				}
				container.find(".restoreContainer:first").remove();
				if (container.hasClass("resizable") && container.attr("minimized")=="false") container.containerResize();
			});
		});
	}

	jQuery.fn.mb_resizeTo = function (h,w){
		if (!w) w=$(this).outerWidth();
		if (!h) h=$(this).outerHeight();
		var elHeight= h-$(this).find(".n:first").outerHeight()-($(this).find(".s:first").outerHeight());
		$(this).find(".c:first , .content:first").animate({height: elHeight});
		$(this).animate({"height":h});
		$(this).animate({"width":w});
	}

	jQuery.fn.mb_iconize = function (){
		if ($(this).attr("iconized")=="true"){
			$(this).find(".restoreContainer:first").click();
		}else{
			$(this).iconize();
		}
	}

	jQuery.fn.mb_BringToFront= function(){
		var zi=10;
		$('*').each(function() {
			if($(this).css("position")=="absolute"){
				var cur = parseInt($(this).css('zIndex'));
				zi = cur > zi ? parseInt($(this).css('zIndex')) : zi;
			}
		});
		$(this).css('zIndex',zi+=1);
	}
})(jQuery);

