from enum import Enum

class JobStatus(Enum):
    InProgress = 1
    Completed = 2
    
    def __str__(self):
        translations = {
            JobStatus.InProgress: "В процессе",
            JobStatus.Completed:  "Доставлено",
        }
        return translations[self]