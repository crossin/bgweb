// JavaScript Document


var actualGroup="bar";
var pageIsLoaded=false;
var bgN=11;
var bgndPath="images";
var inEvidence=["MistFog2", "mbTabset", "MistFog3"];

$.fn.rndBgnd= function(){
	var n=5;//1+ Math.floor(Math.random()*bgN);
	$(this).css({background: "url("+bgndPath+"/"+n+".jpg) fixed"});
}

var margLeft=120;
var margbottom=220;

$.fn.rndPos= function(anim){
	anim=anim!=0;
	return this.each(function(){
		var ww      =$(document).width()-$(this).outerWidth() -($.browser.opera?380:0)-margLeft;//.find(".n")
		var wh      =$(document).height()-$(this).outerHeight()-($.browser.opera?380:0)-margbottom;
		var rndL    =   Math.floor(Math.random()*ww);
		var rndT    =   Math.round(Math.random()*wh);
		if (anim)
			$(this).animate({left:rndL, top:rndT},150); //function() {$(this).attr("minimized")=="true"? $(this).minimize():null}
		else
			$(this).css({left:rndL, top:rndT});
	})
}

function redirectToPage(){
	var location=self.location.href.split("#");
	var redirectPage=location[1];
	var url="demo/jquery."+redirectPage+"/";
	if (redirectPage!=undefined && redirectPage.length>0)
		loadPage(url,"develop")
}

var winw=$(window).width();
var winh=$(window).height();

var doOnResize=function(){
	if(pageIsLoaded || !switched) return;
	$(document).stopTime("doRes");
	$(document).oneTime(100,"doRes",function(){
		//$(".containerPlus").not(".navigator").not(".doc").adjastPos();
		winw=$(window).width();	winh=$(window).height();
	});
}

$.fn.adjastPos= function(){
	var nww=$(window).width();
	var nwh=$(window).height();

	this.each(function(){
		var l= ((($(this).offset().left+$(this).outerWidth())*nww)/winw)-$(this).outerWidth();
		var t= ((($(this).offset().top+$(this).outerHeight())*nwh)/winh)-$(this).outerHeight();
		l=(l>margLeft)?l:margLeft;
		t=(t>0)?t:0;
		$(this).animate({left:l, top:t},550)
	});
}

$.fn.adjustToMid= function(){
    var cardw  = 600;
    var cardh  = 300;

	this.each(function(){
		var centerl= winw / 2;
		var centerh= winh / 2;
		
        var l = centerl - cardw/2;
        var h = centerh - cardh/2;
        
        l=(l>margLeft)?l:margLeft;
		h=(h>0)?h:0;
		$(this).animate({left:l, top:h},550)
	});
}


var switched=false;
$.fn.switchCard= function(tag,collapse){
	collapse= collapse != 0;
	switched=true;
	//collapse=false;
	$("#ribbonbar").find(".button").removeClass("selected");
	$("#ribbonbar").find(tag).addClass("selected");
	if (tag==".showAll") tag=".containerPlus";
	return this.each(function(){
		var scheda=this;
		if ($(scheda).is(".doc")) return;
		if (!$(scheda).is(".navigator") ){
			if ($(scheda).is(tag)){
				if (collapse && ($(scheda).attr("minimized")=="false" || ($(scheda).is(".info") && $(scheda).attr("minimized")=="false" && tag!=".info"))) $(scheda).find('.minimizeContainer').click();
				if ($(scheda).is(".info") && $(scheda).attr("minimized")=="true" && tag !=".containerPlus") $(scheda).find('.minimizeContainer').click();
				$(scheda).fadeIn(400,function(){if ($(scheda).is (".info")) $(scheda).mb_BringToFront();});
				//$(document).oneTime(400,"rnd",function(){$(scheda).rndPos()});
			}else{
				if ($(scheda).attr("minimized")=="false") $(scheda).find('.minimizeContainer').click();
				$(scheda).fadeOut(400,function(){});
			}
		}
	})
}

var actualPage="";

var loadPage=function(page,group){
	actualGroup=group?group:"";
	if (page && page.indexOf("http")>-1){
		$("#pageContent").css({height:"100%", background:"#fff"});
		$("#bar #newWin").attr("href",page).attr("target","_blank");
	}else{
		$("#pageContent").css({height:"100%", background:"transparent"});
		actualPage=page;
		page=group?page+="demo.html":page;
		$("#newWin").css("display",group?"":"none");
	}
	$("#pageContent").append("<iframe id='iframe' style='position:absolute;bottom:0;left:0;width:100%;height:100%;border:0;' src=''> </iframe> ");
	$(".banners").fadeOut (400);
	$("#ribbonbar").fadeOut(400, function(){
		$("#"+actualGroup+"bar").fadeIn(400);
	})
	$(".containerPlus").not(".navigator").each(function(){
		$(this).attr("oldL",$(this).offset().left);
		$(this).animate({
			left:-1000
		}, 400,"linear",function(){
			$("#back").animate({opacity:.6,left:-20},100)
			$("#back").fadeIn(500);
		});
	});
	setTimeout(function(){
		if (page!=undefined) $("#iframe").attr("src",page);
		$("#pageContent").css({bottom:0, left:0}).fadeIn(800,function(){$("#back").animate({opacity:.6,left:-100},100)});//$("body").rndBgnd();

	},1000);
	pageIsLoaded=true;
}

var unloadPage=function(){
	$("#back").fadeOut(500);
	$("#"+actualGroup+"bar").fadeOut(400, function(){$("#ribbonbar").fadeIn(400)})
	actualGroup="";
	$("#pageContent").fadeOut(400,function(){
		$("#iframe").remove();
		return $(".containerPlus").not(".navigator").each(function(){
			$(this).animate({
				left:$(this).attr("oldL")
			}, 400,"linear",function(){});//$(this).rndPos()
		})
	})
	$(".banners").fadeIn (400);
	pageIsLoaded=false;
	$(".doc").fadeOut();

}

$.fn.showDoc=function(){
	window.open("http://pupunzi.wordpress.com/category/jquery/","_blank");
}
$.fn.mb_BringToFront= function(){
	var zi=10;
	$('*').each(function() {
		if($(this).css("position")=="absolute"){
			var cur = parseInt($(this).css('zIndex'));
			zi = cur > zi ? parseInt($(this).css('zIndex')) : zi;
		}
	});

	$(this).css('zIndex',zi+=10);
}

function makeContainersFromJson(json){
	$.getJSON(json,
		function(data){
			$.each(data.containers,
				function(i,item){
					$("<div/>")
						.attr({id:item.id, width:item.width, height:item.height, buttons:item.buttons,skin:item.skin})
						.css({left:-2500})
						.addClass("containerPlus")
						.addClass(item.properties)
						.addClass(item.type)
						.append(
						$("<div/>").addClass("no").append(
							$("<div/>").addClass("ne").append(
								$("<div/>").addClass("n").html("<a href=\"#\" onclick=\"$(this).parents('.containerPlus').find('.minimizeContainer').click();\">"+item.title+"</a>")
								)
							).append(
							$("<div/>").addClass("o").append(
								$("<div/>").addClass("e").append(
									$("<div/>").addClass("c").append(
										$("<div/>").addClass("content").html(
											(item.image?"<img src=\""+item.image+"\" alt=\""+item.id+"\" />":"")+
											item.description +
											(item.link?"<p style=\"float:right;\"><a class=\"button special\" href=\"#\" onclick=\"loadPage('"+item.link.url+"'"+(item.type=="develop"?",'"+item.type+"'":"")+")\"><span>"+item.link.desc+"</span></a></p>":"")
											)
										)
									)
								)
							).append(
							$("<div/>").append(
								$("<div/>").addClass("so").append(
									$("<div/>").addClass("se").append(
										$("<div/>").addClass("s")
										)
									)
								)
							)
						)
						.appendTo(item.parent)
						.buildContainers({
						containment:"document",
						elementsPath:"elements/"
					});
				});
		});
}

$(function(){
	//makeContainersFromJson("containers.json");
	$("body").rndBgnd();
	$(".containerPlus .button").each(function(){if ($(this).attr("href")) $(this).attr("href","#");})
	$(".navigator .button").one("click",function(){$("#startText").slideUp("slow")})
	if (!$.browser.msie) $(".banners img").css({cursor:"pointer",opacity:.7}).bind("mouseover",function(){$(this).css("opacity",1)}).bind("mouseout",function(){$(this).css("opacity",.7)});
	$(".doc").buildContainers();
	//$(".containerPlus").not(".navigator").css({left:-1000})
	//$(".containerPlus").switchCard(".develop",0);
	$(".navCardlist")
        .css({opacity:.6})
        .hover( function(){
                    $(this).animate( {opacity:.6,left:-20},100)
                },  
                function(){
                    $(this).animate( {opacity:.6,left:-100},100)
                }
        );
	//$(window).resize(doOnResize);
	//setTimeout(function(){$(".containerPlus").switchCard(".showAll",1)},2500);
	//setTimeout(function(){redirectToPage();},5500);
	//setTimeout(function(){
		//for (var i in inEvidence){
			//$("#"+inEvidence[i]).mb_BringToFront();
			//if ($("#"+inEvidence[i]).offset().top+600>$(window).height())$("#"+inEvidence[i]).animate({top:$("#"+inEvidence[i]).offset().top-300});

			//$("#"+inEvidence[i]).find('.minimizeContainer:first').click();}
	//},4000);


});

