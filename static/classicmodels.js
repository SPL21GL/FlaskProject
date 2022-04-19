function deleteProduct(element) {
    if(window.confirm("Wollen Sie das Item wirklich löschen"))
    {
        element.parentElement.submit();
    }
}

function deleteOrder(element) {
    if(window.confirm("Wollen Sie das Item wirklich löschen"))
    {
        element.parentElement.submit();
    }
}


/* 
document.querySelector("a[href='/products']").classList.add("active")
*/