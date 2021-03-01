public class Matrix {
	
	private float[][] matx;
	
	//constructor 1
	public Matrix(int a, float v) {
		this.matx = new float[a][a];	
		for(int i=0;i<a;i++)
			for(int j=0;j<a;j++)
				this.matx[i][j]=v;
	}
	public Matrix(int a, int b, float v) {
		this.matx = new float[a][b];
		for(int i=0;i<a;i++)
			for(int j=0;j<b;j++)
				this.matx[i][j]=v;
	}
	public Matrix(int a, int b) {
		this.matx = new float[a][b];	
		for(int i=0;i<a;i++)
			for(int j=0;j<b;j++)
				this.matx[i][j]=(float) 0.0;
	}
	public Matrix(int a) {
		this.matx = new float[a][a];
		for(int i=0;i<a;i++)
			for(int j=0;j<a;j++)
				this.matx[i][j]=(float) 0.0;
	}
	
	//2 add()
	Matrix add(Matrix objB) {
		int rownumA = this.getrows();
		int colnumA = this.getcols();
		
		int rownumB = objB.getrows();
		int colnumB = objB.getcols();
		
		Matrix opObj;
		
		if((rownumA==rownumB) && (colnumA==colnumB)) {
			opObj = new Matrix(rownumA,colnumA);
			
			for(int i=0;i<rownumA;i++) {
				for(int j=0; j<colnumA; j++) {
					opObj.matx[i][j] = this.matx[i][j]+objB.matx[i][j];
				}
			}
		}else {
			System.out.println("Matrices cannot be added");
			opObj = new Matrix(1,1,0);
		}
		
		return opObj;
	}
	
	//3 matmul()
	Matrix matmul(Matrix objB) {
		int rownumA = this.getrows();
		int colnumA = this.getcols();
		
		int rownumB = objB.getrows();
		int colnumB = objB.getcols();

		Matrix opObj;
		
		if(colnumA==rownumB) {
			opObj = new Matrix(rownumA, colnumB);
			for(int i=0;i<rownumA;i++) {
				for(int j=0; j<colnumB; j++) {
					opObj.matx[i][j] = 0;
					for(int k=0; k<colnumA; k++)
						opObj.matx[i][j] += this.matx[i][k]*objB.matx[k][j];
				}
			}
			
		}else {
			System.out.println("Matrices cannot be multiplied");
			opObj = new Matrix(1,1,0);
		}
		
		return opObj;
	}
	
	//4 scalarmul()
	void scalarmul(int scalval) {
		int rownum = this.getrows();
		int colnum = this.getcols();
		
		for(int i=0;i<rownum;i++) {
			for(int j=0; j<colnum; j++) {
				this.matx[i][j] *= scalval;
			}
		}
	}
	
	//5 getrows()
	int getrows() {
		return this.matx.length;
	}
	
	//6 getcols()
	int getcols() {
		return this.matx[0].length;
	}
	
	//7 getelem()
	float getelem(int r, int c) {
		try {
			return this.matx[r][c];
		}catch(IndexOutOfBoundsException e) {
			System.out.println("Index out of bound");
			return (float)-100;
		}
	}
	
	//8 setelem()
	void setelem(int r, int c, float val){
		try {
			this.matx[r][c] = val;
		}catch(IndexOutOfBoundsException e) {
			System.out.println("Index out of bound");
		}
	}
	
	//9 printmatrix()
	void printmatrix() {
		int rownum = this.getrows();
		int colnum = this.getcols();
		
		for(int i=0;i<rownum;i++) {
			String rowval = "";
			for(int j=0; j<colnum; j++) {
				rowval += this.matx[i][j]+" ";
			}
			rowval=rowval.trim();
			System.out.println(rowval);
		}
	}

}
