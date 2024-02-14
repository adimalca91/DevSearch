// // Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });


// let alertWrapper = document.querySelector('.alert')
// let alertClose = document.querySelector('.alert__close')

// if (alertWrapper) {
//   alertClose.addEventListener('click', () =>
//     alertWrapper.style.display = 'none'
//   )
// }

// ADI - notice the code above does NOT work for the red error alerts therefore we need to loop 
//       through all of them and click them one by one.
// NOTE - a lot of people had this issue and Yasha person fidured it out!
// Also NOTICE - the x button work on internet Microsoft edge but NOT on my google chrome! FIX!!! THIS ONLY WORKED ON GOOOGLE CHROME AFTER I UPDATED
// THE CHROME VERSION AND CLEARED ALL CACHE!

let alertWrapper = document.querySelectorAll('.alert'); 
let alertClose = document.querySelectorAll('.alert__close');
  
if(alertWrapper){
    for (let i = 0; i < alertClose.length; i++) {
     alertClose[i].addEventListener('click', ()=>{
       alertWrapper[i].style.display = 'none'});
       }
  } 

