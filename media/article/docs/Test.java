class Test{

public static void main(String []args){
int n = 4;
int sum = n*1;
for (int j=1;j<n;j++){

	if (j <= n){
		sum =  sum + (j*(n-(j+1)));
//		System.out.println(sum);
		
	}
	 System.out.println(sum);
}

}
}

