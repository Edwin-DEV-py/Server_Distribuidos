from spyne.model.primitive import Integer, Unicode
from spyne.model.complex import ComplexModel

class File(ComplexModel):
    id = Integer
    fileName = Unicode
    folderParent = Integer
    userId = Unicode
    createdAt = Unicode
    type = Unicode
    paths = Unicode.customize(max_occurs='unbounded')

class ResponseData(ComplexModel):
    data = File.customize(max_occurs='unbounded')
    TotalStorage = Integer
