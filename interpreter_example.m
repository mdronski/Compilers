# control flow instruction

#N = 3;
#M = 3;
#for i = 1:N {
#    for j = i:M {
#        print i," ", j;
#    }
#}

k = 15;
while(k>0) {
    if(k<5)
        print "xd";
    else if(k<10)
        print "xd2";
    else
        print "xd3";

    k = k - 1;
    print k;
}
