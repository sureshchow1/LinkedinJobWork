class Test1{

   public static void main(String []args){
	String  num = "182";
        StringBuilder latest_num = new StringBuilder(num);
        // System.out.println(num.charAt(0));
//int i = num.length()-1;
	for(int i=num.length()-1; i>=1; i--){
	  boolean modified = false; 
	   for(int j=i-1; j>=0; j--){
             // System.out.println(num.charAt(j));
	      if (num.charAt(i) > num.charAt(j)){
		  modified = true;
		  // latest_num.setCharAt(i, num.charAt(j));
		  latest_num.setCharAt(j, num.charAt(i));
		  break;
	       }
		if (modified){
			break;
		}
	      
	}

	System.out.println(latest_num);
	
	}		

   }
}
