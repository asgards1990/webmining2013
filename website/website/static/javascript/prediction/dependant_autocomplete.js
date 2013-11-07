// Lien entre genre1 et keywords

//$.ajaxSetup( {headers : {"X-Requested-With" : "Ajax"}});

$(document).ready(function() {
	var dict={};
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1SelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre1', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            dict['genre1_id'] = value[0];
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        } else {
            // If value is empty, empty autocomplete.data
            dict['genre1_id'] = -2;
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })

// Lien entre genre2 et keywords

    $('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre2SelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre2', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            dict['genre2_id'] = value[0];
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        } else {
            // If value is empty, empty autocomplete.data
            dict['genre2_id'] = -2;
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })
});

// Lien entre de genre 1 vers genre 2

$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1SelectElement = $(this);
        var genre2SelectElement = $('#' + $(this).attr('id').replace('genre1', 'genre2'));
        var genre2WidgetElement = genre2SelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            genre2WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre1_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            genre2WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre1_id': -2,
            };
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(genre2WidgetElement, 'data is', genre2WidgetElement.yourlabsWidget().autocomplete.data)
    })
});

// Lien entre de genre 2 vers genre 1

$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre2SelectElement = $(this);
        var genre1SelectElement = $('#' + $(this).attr('id').replace('genre2', 'genre1'));
        var genre1WidgetElement = genre1SelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            genre1WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre2_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            genre1WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre2_id': -2,
            };
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(genre1WidgetElement, 'data is', genre1WidgetElement.yourlabsWidget().autocomplete.data)
    })
});



function ajoutKeywordSuggest(keyword) {
    var newKeyword = document.createElement('span');
    newKeyword.className="newKeyword";


    var newName = document.createElement('span');
    newName.className="name";

    newName.appendChild(document.createTextNode(keyword));

    var newDelete = document.createElement('span');                               
    newDelete.className="delete";

    var newImg1 = document.createElement('img');
    newImg1.className="add1";
    newImg1.src="../pesto/static/img/prediction/AddGrey.png";
   

    var newImg2 = document.createElement('img');
    newImg2.className="add2"; 
    newImg2.src="../pesto/static/img/prediction/AddBlue.png";

    keywordClick(newImg1);
    newKeyword.appendChild(newDelete);
    newKeyword.appendChild(newName);

    newDelete.appendChild(newImg1);
    newDelete.appendChild(newImg2);

    document.getElementById("keywordSuggest").appendChild(newKeyword);

};

function keywordClick (icone) {
    $(icone).click(function(){
        if((this.className=="remove div")&&(this.id=="suggest")){            
            var element = this.parentNode;
            var remove = document.createElement('span');
            var newImg1 = document.createElement('img');
            newImg1.className="add1";
            newImg1.src="../pesto/static/img/prediction/AddGrey.png";
   

    var newImg2 = document.createElement('img');
    newImg2.className="add2"; 
    newImg2.src="../pesto/static/img/prediction/AddBlue.png";
            suggestion = document.getElementById("keywordSuggest");

            this.parentNode.parentNode.removeChild(element);

            element.getElementsByClassName("suppress1")[0].src="../pesto/static/img/prediction/AddGrey.png";
            element.getElementsByClassName("suppress2")[0].src="../pesto/static/img/prediction/AddBlue.png";
            element.className="newKeyword";
            suggestion.appendChild(element);
            }

        else {
            if (this.className=="remove div") {
            this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
               }
            else {
                var element = this.parentNode.parentNode;
                var remove = document.createElement('span');
                var text = document.createTextNode(element.getElementsByClassName("name")[0].textContent);
                var xxx = document.createTextNode("X");
                alert(element.getElementsByClassName("name")[0].textContent);
                keywords = document.getElementById("id_keyword-deck");

                this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);

                if (element.hasChildNodes()){
                     while (element.childNodes.length>=1)
                         {element.removeChild(element.firstChild);
                    }
               };

                remove.className="remove div";
                remove.id="suggest";
                remove.style.display="inline";
                element.className="div hilight";

                element.appendChild(remove);
                element.appendChild(text);
                keywords.appendChild(element);
                };
            };

    });
};


function callback_suggest (resp) {
    if (resp.success) {
        for (k=0; k<resp.results.length; k++) {
            ajoutKeywordSuggest(resp.results[k][1]);
        }
    }
    else {
        alert('Error : ' + resp.error);
    }
}


$(document).ready(function() {
    ajoutKeywordSuggest("test");
	
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1 = $('#id_genre1');
        var genre2 = $('#id_genre2');
        var id1 = genre1.val();
        var id2 = genre2.val();
        urlSubmit = 'http://senellart.com:8080/suggest/';
		var bloc = document.getElementById("keywordSuggest");

        if (id1) {
            var value1 = $('#id_genre1-deck').clone().children().children().remove().end().text();

          
        
            if (id2) {
                var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
				
				 if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };				
				
				
				 var args1 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value1]]};
				 var args2 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value2]]};
				 $.post(urlSubmit, "json_request="+JSON.stringify(args1), callback_suggest, "json");
				 $.post(urlSubmit, "json_request="+JSON.stringify(args2), callback_suggest, "json");
			
				
                
                }
            else {
               var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value1]]};
			   if (bloc.hasChildNodes()) {
               while (bloc.childNodes.length>=1)
               {bloc.removeChild(bloc.firstChild);
                }
               };
              
               $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");
	
	                  
                };
            }
        else {if (id2) {
            var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
			var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value2]]};
            
			
			
				if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };
			   
			  $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");
			   
	
                };
			};
		});
		
		$('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre1 = $('#id_genre1');
        var genre2 = $('#id_genre2');
        var id1 = genre1.val();
        var id2 = genre2.val();
        urlSubmit = 'http://senellart.com:8080/suggest/';
		var bloc = document.getElementById("keywordSuggest");

        if (id1) {
            var value1 = $('#id_genre1-deck').clone().children().children().remove().end().text();

          
        
            if (id2) {
                var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
				
				 if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };				
				
				
				var args1 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value1]]};
				var args2 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value2]]};
				$.post(urlSubmit, "json_request="+JSON.stringify(args1), callback_suggest, "json");
				$.post(urlSubmit, "json_request="+JSON.stringify(args2), callback_suggest, "json");
			
				
                
                }
            else {
               var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value1]]};
			   if (bloc.hasChildNodes()) {
               while (bloc.childNodes.length>=1)
               {bloc.removeChild(bloc.firstChild);
                }
               };
              
              $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");


	                  
                };
            }
        else {if (id2) {
            var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
			var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value2]]};
            
			
			
				if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };
			   
			  $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");

                };
			};
		});
	});
				
				
            
                          
                        
                    
            
