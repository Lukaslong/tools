#include <iostream>
#include <algorithm>

int[] bubblesort(int[] arr)
{
    if(arr.length==0)
    {
        return arr;
    }
    for(int i=0;i<arr.length-1;i++)
    {
        for(int j=0;j<arr.length-1-i;j++)
        {
            if(arr[j]>arr[j+1])
            {
                int temp=arr[j];
                arr[j]=arr[j+1];
                arr[j+1]=temp;
            }
        }
    }
    return arr;
}

int[] selectsort(int[] arr)
{
    int len=arr.length;
    if(len==0){
        return arr;
    }
    for(int i=0;i<len;i++){
        int min_index=i;
        for(int j=i;j<len;j++)
        {
            
            if(arr[j]<arr[min_index])
            {
                min_index=j;
            }
        }
        int temp=arr[i];
        arr[i]=arr[min_index];
        arr[min_index]=temp;
    }
    return arr;

}

int[] insertsort(int[] arr)
{
    int len=arr.length;
    for(int i=0;i<len-1;i++)
    {
        int j=i;
        current=arr[i+1];
        while(j>=0 && current<arr[j])
        {
            arr[j+1]=arr[j];
            j--;
        }
        arr[j+1]=current;
    }
    return arr;
}
