A = [[1,2,3], [4,5,6]];
B = [[1,2],[3, 4],[5,6]];

D1 = A.+B' ; # add element-wise A with transpose of B
D2 = A.-B' ; # substract element-wise A with transpose of B
D2 *= A.*B ; # multiply element-wise A with transpose of B
D2 /= A./B'; # divide element-wise A with transpose of B

print D1;
print D2;
print D3;
print D4;