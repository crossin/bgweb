function getCycledCardDeck( url){

    $('#cardlist').empty();
    $('#cardlist').load(url,'',function(){
        $('#cardlist').cycle({ 
            fx:    'shuffle', 
            shuffle: { 
                top:  -200, 
                left:  200 
            }, 
            //fx:     'fade',
            delay: -1000 ,
            
            cleartypeNoBg:  true,
            
            next:'#nextCard', 
            prev:'#prevCard',
            pause:1 
        });
        
    }) 
}

function getRecommendedCard(){
    $('#cardlist').empty();
    $('#cardlist').load('/recommended');
}

var isCycling = true;

function toggleCycle(){
    isCycling = !isCycling;
    if( isCycling){
        $('#cardlist').cycle('resume');
        $('#tcycle span').html('stop cycle');
    }
    else{
        $('#cardlist').cycle('pause');
        $('#tcycle span').html('begin cycle');
    }
    
}

$(document).ready(function() {	
	$("#open").click(function(){
		$("div#panel").slideDown("fast");	
	});	
	
	$("#close").click(function(){
		$("div#panel").slideUp("fast");	
	});		
	
	$("#toggle a").click(function () {
		$("#toggle a").toggle();
	});	
    
    getCycledCardDeck('/list?card=1');
    
    

    $('#cardlist').adjustToMid();    
    
    $('#homesetting').empty();
    $('#homesetting').load('/namelist/');
    
    
    $('#submit_config').click( function(){
        var selectedbbsname = $("input[name='rdconfig'][checked]").val();
        $.cookie('selectedtop1', selectedbbsname ,{ expire:-1, path:'/' ,domain:'bbstop10.appspot.com' } );
        alert('your selection '+ selectedbbsname +' saved');          
    });
    
    
});