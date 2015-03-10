class User < ActiveRecord::Base
  has_many :downloads
  has_many :links, through :downloads
end
