#include <Arduino.h>
#include <Vector.h>

const int ELEMENT_COUNT_MAX = 5;

void setup()
{
  Serial.begin(115200);
  delay(1000);

}

void loop()
{
  int storage_array[ELEMENT_COUNT_MAX];
  Vector<int> vector;
  vector.setStorage(storage_array);
  Serial.print( "vector.max_size(): ");
  Serial.println(vector.max_size());
  Serial.print("vector.size()");
  Serial.println(vector.size());
  Serial.print("Vector:");
  //Serial.println(vector);
  delay(5000);

  vector.push_back(10);
  vector.push_back(8);
  vector.push_back(7);
  Serial.print( "vector.max_size(): ");
  Serial.println(vector.max_size());
  Serial.print("vector.size()");
  Serial.println(vector.size());
  Serial.print("Vector:");
  //Serial.println(vector);
  vector.remove(0);
  Serial.println("Remove(0)");
  Serial.print( "vector.max_size(): ");
  Serial.println(vector.max_size());
  Serial.print("vector.size()");
  Serial.println(vector.size());
  Serial.print("Vector:");
  //Serial.println(vector);
  vector.remove(1);
  Serial.println("Remove(1)");
  Serial.print( "vector.max_size(): ");
  Serial.println(vector.max_size());
  Serial.print("vector.size()");
  Serial.println(vector.size());
  Serial.print("Vector:");
  //Serial.println(vector);
  delay(10000);
  /*
  int storage_array2[ELEMENT_COUNT_MAX];
  Vector<int> vector2(storage_array2);
  vector2.push_back(1);
  vector2.push_back(2);
  vector2.push_back(4);
  vector2.pop_back();
  Serial << "vector2.max_size(): " << vector2.max_size() << endl;
  Serial << "vector2.size(): " << vector2.size() << endl;
  Serial << "vector2:" << endl;
  Serial << vector2 << endl;
  delay(1000);

  int storage_array3[ELEMENT_COUNT_MAX];
  storage_array3[0] = 3;
  storage_array3[1] = 5;
  Vector<int> vector3(storage_array3);
  Serial << "vector3.max_size(): " << vector3.max_size() << endl;
  Serial << "vector3.size(): " << vector3.size() << endl;
  Serial << "vector3:" << endl;
  Serial << vector3 << endl;
  delay(1000);

  int storage_array4[ELEMENT_COUNT_MAX];
  storage_array4[0] = 3;
  storage_array4[1] = 5;
  Vector<int> vector4(storage_array4,2);
  Serial << "vector4.max_size(): " << vector4.max_size() << endl;
  Serial << "vector4.size(): " << vector4.size() << endl;
  Serial << "vector4:" << endl;
  Serial << vector4 << endl;
  delay(1000);

  int storage_array5[1];
  Vector<int> vector5(storage_array5);
  Serial << "vector5.max_size(): " << vector5.max_size() << endl;
  Serial << "vector5.size(): " << vector5.size() << endl;
  Serial << "vector5:" << endl;
  Serial << vector5 << endl;
  delay(1000);

  int storage_array6[ELEMENT_COUNT_MAX];
  Vector<int> vector6(storage_array6);
  vector6.assign(ELEMENT_COUNT_MAX-1,8);
  Serial << "vector6:" << endl;
  Serial << vector6 << endl;
  delay(1000); */
}
