class Link < ActiveRecord::Base
  belongs_to :version
  has_many :downloads
  has_many :users, through :downloads
end
