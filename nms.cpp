#include <iostream>
#include <algorithm>
#include <vector>

struct Box{
    float x1;
    float y1;
    float x2;
    float y2;
};

struct Object{
    Box box;
    float score;
    int label;
};

inline bool compare_score(Object obj1,Object obj2)
{
    return (obj1.score>obj2.score);
}

float iou(Box b1,Box b2)
{
    float x1=std::max(b1.x1,b2.x1);
    float y1=std::max(b1.y1,b2.y1);
    float x2=std::min(b1.x2,b2.x2);
    float y2=std::min(b1.y2,b2.y2);
    float public_area=(x2-x1)*(y2-y1);
    return (public_area/((b1.x2-b1.x1)*(b1.y2-b1.y1)+(b2.x2-b2.x1)*(b2.y2-b2.y1)-public_area);
}

std::vector<Object> nms(std::vector<Object>& objects,float threshold)
{
    std::vector<Object> results;

    while(objects.size()>0)
    {
        std::sort(objects.begin(),objects.end(),compare_score);
        results.push_back(objects[0]);
        size_t i=1;
        while(i<objects.size())
        {
            float iou_value=iou(objects[0].box,objects[i].box);
            if(objects[0].label==objects[1].label && iou_value>=threshold)
            {
                objects.erase(objects.begin()+i);
            }
            else
            {
                i++;
            }
        }
        objects.erase(objects.begin());
    }

    return results;
}

int main()
{


    return 1;

}