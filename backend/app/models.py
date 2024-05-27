from app import db

class Cite(db.Model):
    MammalId = db.Column(db.Integer, primary_key=True)
    PublicationId = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<CiteId {}>'.format(self.PublicationId)

class Favor(db.Model):
    UserId = db.Column(db.Integer, primary_key=True)
    MammalId = db.Column(db.Integer, primary_key=True)
    FavorTime = db.Column(db.DateTime)

    def __repr__(self):
        return '<UserId {} favors MammalId {}>'.format(self.UserId, self.MammalId)


class Habitat(db.Model):
    HabitatId = db.Column(db.Integer, primary_key=True)
    CountryName = db.Column(db.String(255))
    ContinentName = db.Column(db.String(255))

    def __repr__(self):
        return '<Habitat {}>'.format(self.HabitatId)


class Institution(db.Model):
    InstitutionId = db.Column(db.Integer, primary_key=True)
    InstitutionName = db.Column(db.String(255))
    AbbrName = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Website = db.Column(db.String(255))

    def __repr__(self):
        return '<Institution {}>'.format(self.InstitutionName)


class Locate(db.Model):
    MammalId = db.Column(db.Integer, primary_key=True)
    HabitatId = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<MammalId {} locates in HabitatId {}>'.format(self.MammalId, self. HabitatId)


class Mammal(db.Model):
    MammalId = db.Column(db.Integer, primary_key=True)
    SciName = db.Column(db.String(255))
    Extinct = db.Column(db.Integer)
    GenusName = db.Column(db.String(255))
    FamilyName = db.Column(db.String(255))
    OrderName = db.Column(db.String(255))
    InstitutionId = db.Column(db.Integer)

    def __repr__(self):
        return '<Mammal {}>'.format(self.SciName)


class Publication(db.Model):
    PublicationId = db.Column(db.Integer, primary_key=True)
    PublicationName = db.Column(db.String(1023))
    AuthorName = db.Column(db.String(1023))
    PublishYear = db.Column(db.String(255))
    PublishLink = db.Column(db.String(2047))

    def __repr__(self):
        return '<Publication {}>'.format(self.PublicationName)


class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.UserName)

