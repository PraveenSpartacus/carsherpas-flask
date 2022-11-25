// Increment Section

function incrementFun(n,ele){
    var count = 0;
    // console.log(n)
    var interval = setInterval(()=>{
        // console.log(n);
        ele.innerText = "+" + count.toString() + "%";
        count++;
        // console.log(interval)
        if(count == n+1){
            clearInterval(interval);
        }
    },30)    
}



let options = {
    root: null,
    rootMargin: '0px',
    threshold: 1
}

  
let observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry)=>{
        if(entry.intersectionRatio == 1){
            console.log(entry.intersectionRatio)
            incrementFun(45,document.getElementById("inc1"));
            incrementFun(32,document.getElementById("inc2"));
            incrementFun(27,document.getElementById("inc3"));
            console.log("increment over")
            observer.unobserve(entry.target);
        }
    })
}, options);
target = document.getElementById("inc1")
observer.observe(target)