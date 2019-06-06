/* PyObject */
#define PyObject_HEAD \
    int refCount; \
    struct tagPyTypeObject *type

#define PyObject_HEAD_INIT(typePtr) \
    0, typePtr

typedef struct tagPyObject
{
    PyObject_HEAD;
}PyObject;

/* PyTypeObject */
typedef void(* PrintFun)(PyObject* object);
typedef PyObject* (*AddFun)(PyObject* left, PyObject* right);
typedef long (*HashFun)(PyObject* object);

typedef struct tagPyTypeObject
{
    PyObject_HEAD;
    char* name;
    PrintFun print;
    AddFun add;
    HashFun hash;
};

/* PyIntObject */
typedef struct tagPyIntObject
{
    PyObject_HEAD;
    int value;
}PyIntObject;

