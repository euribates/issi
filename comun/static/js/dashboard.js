function main() {
   console.log("main starts"); 
   const hamburger = document.getElementById("hamburger");
   const chevron = document.getElementById("chevron");
   const sidebar = document.getElementById("sidebar");
   hamburger.addEventListener("click", function (evt) {
      chevron.classList.toggle('bi-chevron-double-left');
      chevron.classList.toggle('bi-chevron-double-right');
      sidebar.classList.toggle('expanded');
      });
   console.log("main ends"); 
   }

main();
