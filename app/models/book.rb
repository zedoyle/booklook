class Book < ActiveRecord::Base
  has_many :versions
end
