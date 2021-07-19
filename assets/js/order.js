var order_list={};
var items_list = {};
var order=[];
var txt="";
var total;
function decreaseval(x,y){
           var value = document.getElementById(x).value;
           if (value>0 && value<=10){
           value--;
           document.getElementById(x).value = value;
           order_list[x]=value;
           console.log(value,x)
           if (value==0){
           delete items_list[x];
           delete order_list[x];
           console.log(items_list, order_list);
           }
           }
           }

function increaseval(x,y){
        var value = document.getElementById(x).value;
         if (value>=0 && value<10){
            value++;
            document.getElementById(x).value = value;
            console.log(value, x);
            order_list[x]=value;

            check_key = 'x' in items_list;
            if (check_key==false){
            items_list[x]=y;
            console.log(items_list,order_list);
            }
            }
            }

function conf_order(){
    var osize=Object.keys(order_list).length;
    if (osize >0){
    var i;
    for (i in order_list){
        order.push(order_list[i]+" "+i)
        }
    }else{console.log("Nothing to show")}
    console.log(order);

    for(i=0; i<order.length; i++){
    if(i<=(order.length)-2){
    txt+=order[i]+" , "
    }else{
    txt+=order[i]
    }}
    console.log(txt)
     document.getElementById('ordered_list').value=txt

}

function reset(){
txt="";
document.getElementById('ordered_list').innerHTML="";
}
//var myModal = document.getElementById('myModal')
//var myInput = document.getElementById('myInput')
//
//myModal.addEventListener('shown.bs.modal', function () {
//  myInput.focus();
//})
