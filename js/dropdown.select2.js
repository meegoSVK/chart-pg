$(document).ready(function(){

 $("#selSensor").select2({
  ajax: { 
   url: "http://localhost/graphs/api/sensor-list.php",
   type: "post",
   dataType: 'json',
   delay: 250,
   data: function (params) {
    return {
      searchTerm: params.term // search term
    };
   },
   processResults: function (response) {
     return {
        results: response
     };
   },
   cache: true
  }
 });
 

});