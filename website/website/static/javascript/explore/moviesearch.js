
/*$(document).ready(function(){

critereEnable = false;
	function createClick(nom) {

		if (nom=="movieinput") {
        			
			$("#movieinput").keyup(function(event){
			if(event.keyCode == 13){
			var p = this.parentNode;
			var element = this.parentNode.parentNode;
			var value = this.value
			var textNode = document.createTextNode(value)
			p.removeChild(this);

			p.appendChild(textNode);
			element.getElementsByTagName("img")[0].src="http://goo.gl/8IrUDR";

			var deleteicon = document.createElement('div');
			deleteicon.className = "deleteicon";
			deleteicon.style="cursor: pointer;"; 

			var image = document.createElement('img');
			image.style="max-height:1.4em;max-width:1.4em";
			image.src="http://goo.gl/61lXjQ";
			image.alt="Edit";

			deleteicon.appendChild(image);
			element.appendChild(deleteicon);
			
			if (critereEnable==false) {
				var tabCriteres=document.getElementById("filters").getElementsByTagName("input");
				var formGenres=document.getElementById("genres").getElementsByTagName("form")[0];
				var formBudget=document.getElementById("slider-range");
				var formReviews=document.getElementById("ex_1b");
				
			
				critereEnable=true;
			
			for (k=0; k<tabCriteres.length;k++)   {
				tabCriteres[k].disabled=false; 
				formGenres.style.display = "block";
				formBudget.style.display = "block";
				formReviews.style.display = "block";
			
				}
			
			}
	createClick(deleteicon);
			}
		});
		

	}


		else {$(".deleteicon").click(function(){
			var p = this.parentNode.getElementsByTagName("p")[0];
			text = p.textContent;
			var element = this.parentNode;
			var movieinput = document.createElement('input');
			var newP = document.createElement('p');
			element.getElementsByTagName("img")[0].src="../pesto/static/img/explore/questionmark.png";


			element.removeChild(this);
			element.removeChild(p);


			movieinput.id="movieinput";
			movieinput.type="text";
			movieinput.name="actorname"
			movieinput.value=text;
			movieinput.size="12";
			movieinput.style="text-align : left";

			newP.appendChild(movieinput);
			element.appendChild(newP);
	
		createClick("movieinput");
			});	
		}
	};
	
createClick("movieinput");	
	
	

});*/

function ajoutActors (actor) {
    
    var superior = document.getElementById("actors").getElementsByTagName("ul")[0];

    var father = document.createElement('li');
    father.className="listactor";

    
    var paragraph = document.createElement('p');
    paragraph.className="actor";
    paragraph.id = actor.imdb_id;
  

    
    var check = document.createElement('input');
    check.type="checkbox";
    check.name="actor";
    check.value="???";

    var name = document.createElement('span');
    name.className="name";

    var text = actor.name;
    name.appendChild(document.createTextNode(text));
    


    paragraph.appendChild(check);
    paragraph.appendChild(name);

    
    father.appendChild(paragraph);
    superior.appendChild(father);


        $(check).each(function () {
        var self = $(this),
        label = self.next(),
        label_text = label.text();
        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        })
    });

    element = document.getElementById(actor.imdb_id).getElementsByClassName('iCheck-helper')[0];
    element.onclick=function(){changement();};
};


function ajoutTabActors (actors) {
    for (k=0;k<actors.length;k++) {
        ajoutActors(actors[k]);
    };
};

function ajoutGenres (genre) {
    var superior = document.getElementById("genres").getElementsByTagName("ul")[0];

    var father = document.createElement('li');
    father.className="listgenre";

    
    var paragraph = document.createElement('p');
    paragraph.className="genre";
    paragraph.id = genre.id;
  

    
    var check = document.createElement('input');
    check.type="checkbox";
    check.name="genre";
    check.value="???";

    var name = document.createElement('span');
    name.className="name";

    var text = genre;
    name.appendChild(document.createTextNode(text));
    

    paragraph.appendChild(check);
    paragraph.appendChild(name);

    
    father.appendChild(paragraph);
    superior.appendChild(father);


        $(check).each(function () {
        var self = $(this),
        label = self.next(),
        label_text = label.text();
        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        });
    });

    element = document.getElementById(genre.id).getElementsByClassName('iCheck-helper')[0];
    element.onclick=function(){changement();};
};

function ajoutTabGenres (genres) {
    for (k=0;k<genres.length;k++) {
        ajoutGenres(genres[k]);
    };
};

              
                /*<li class="listactor">
                    <p class="actor">
                    <input type="checkbox" name="actor" value="actor1">
                    <span class="name">Cate Blanchett</span>
                    </p>                       
                </li>*/
	
/*function ajoutBudget (budget) {
   var slider = document.getElementById('slider-range');
   $(slider).slider({$( "#amount" ).val( "$" + budget );
      }
    });});
   alert(budget);
   };*/



$(document).ready(function() {
    var isSubmitted = false;
    
    $('body').on('change', '.autocomplete-light-widget select[name$=title_original]', function() {
        
        if (!isSubmitted) {
            isSubmitted = true;
            var film = $('#id_title_original');
            var film_name = $('#id_title_original-deck').clone().children().children().remove().end().text();

            var ul = document.getElementById("actors").getElementsByTagName("ul")[0];
            ul2 = document.getElementById("genres").getElementsByTagName("ul")[0];
            
            if (ul.hasChildNodes())
           {
               while (ul.childNodes.length>=1)
               {ul.removeChild(ul.firstChild);
                }
               };
             if (ul2.hasChildNodes())
           {
               while (ul2.childNodes.length>=1)
               {ul2.removeChild(ul2.firstChild);
                }
               };

        function affichage(film_id) {           
              $.post("/cinema/filmInfo/","film_id="+film_id,function(data){ajoutTabActors(data.actors);ajoutTabGenres(data.genres);});
              };

              
        $.post("/cinema/getId/","film_name="+film_name,function(data){affichage(data);});
            }
        
        else {
            isSubmitted = false;
            
           var ul = document.getElementById("actors").getElementsByTagName("ul")[0];
            ul2 = document.getElementById("genres").getElementsByTagName("ul")[0];
            
            if (ul.hasChildNodes())
           {
               while (ul.childNodes.length>=1)
               {ul.removeChild(ul.firstChild);
                }
               };
             if (ul2.hasChildNodes())
           {
               while (ul2.childNodes.length>=1)
               {ul2.removeChild(ul2.firstChild);
                }
               };
            
            };
        });
    });
            
            
            

