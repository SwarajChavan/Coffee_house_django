var order_list={};
var items_list = {};
var order=[];
var txt="";
var total = 0;
function decreaseval(x,y){
           var value = document.getElementById(x).value;
           if (value>0 && value<=10){
           value--;
           document.getElementById(x).value = value;
           order_list[x]=value;
//           console.log(value,x)
           if (value==0){
           delete items_list[x];
           delete order_list[x];
//           console.log(items_list, order_list);
           }
           }
           }

function increaseval(x,y){
        var value = document.getElementById(x).value;
         if (value>=0 && value<10){
            value++;
            document.getElementById(x).value = value;
//            console.log(value, x);
            order_list[x]=value;

            check_key = 'x' in items_list;
            if (check_key==false){
            items_list[x]=y;
//            console.log(items_list,order_list);
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
    }else{console.log("Nothing to show")
              }
//    console.log(order);

    for(i=0; i<order.length; i++){
    if(i<=(order.length)-2){
    txt+=order[i]+" , ";
    }else{
    txt+=order[i];
    }}
//    console.log(txt);
     document.getElementById('ordered_list').value=txt;

    for(i in items_list){
     total+= (order_list[i]) * (items_list[i]);
     }
//     console.log(total)
     document.getElementById('total').value=total;
}

function reset(){
txt="";
document.getElementById('ordered_list').innerHTML="";
order=[];
order_list_array=[];
items_list_array=[];
total=0;
}

function check_order(){
var str= document.order_form.order.value;
var new_total=document.order_form.total.value;
//console.log(str, total)

if (str!= txt || new_total != total){
alert("OOPS!!!\n Some issue has occurred\n Try placing your order again");
document.order_form.order.value=str;
document.order_form.total= total;
//location.reload()
return false;
}
}